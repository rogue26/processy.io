import json

import more_itertools as mit

from django.shortcuts import render
from django.db.models import Sum
from django.http import JsonResponse
from projects.models import Project
from datetime import timedelta, datetime
from teams.models import TeamMember


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def jsonify_dates(dates):
    return [datetime(_.year, _.month, _.day).isoformat() for _ in dates]


def create_gantt_json(project):
    gantt_data = []
    for task in project.task_set.all():
        gantt_data.append(
            {
                'start': datetime(task.start.year, task.start.month, task.start.day).isoformat(),
                'end': datetime(task.end.year, task.end.month, task.end.day).isoformat(),
                'name': task.name,
                'id': "Task " + str(task.id),
                'progress': 0,
                'dependencies': ["Task " + str(parent_task.id) for parent_task in task.parent_tasks.all()]
            }
        )

    # todo:  do the sorting in python - can't do it in order_by because start is a method
    # sorted(Author.objects.all(), key=lambda a: a.full_name)

    return gantt_data


def create_utilization_schedules(project, resource_constrained=True):
    team_members = TeamMember.objects.filter(project=project)

    project_dates = [date for date in daterange(project.start, project.end)]

    if resource_constrained:
        optimize_utilization_schedules(project)

    utilization_schedules = []
    for team_member in team_members:
        utizilized_days = team_member.calc_utilization_schedule()
        utilization_schedule = [utizilized_days[date] if date in project_dates else 0 for date in project_dates]
        tm_data = {'labels': jsonify_dates(project_dates), 'data': utilization_schedule, }
        utilization_schedules.append(tm_data)



    return utilization_schedules


def optimize_utilization_schedules(project):
    # 1 - determine which tasks can be moved earlier and by how much
    # 2 - for each moveable task, determine if the owner of that task has any unused capacity during that window
    # 3 - for each moveable task for which the owner has bandwidth determine strategy:
    ## A - Opening > 50% of task --> move full task, stretch any overlapping days to satisfy utilization constraints
    ## B - Opening < 50% of task --> do not move task
    # 4 - For each teammember, find any days where where their time is overallocated and stretch those days.
    # 5 - Do a forward gantt calculation to ensure that tasks begin after their parents are completed.

    all_tasks = project.task_set.all()
    tasks_with_leading_gaps = [task for task in all_tasks if task.leading_gap > timedelta(1)]

    for task in tasks_with_leading_gaps:
        dates_in_leading_gap = [date for date in daterange(task.earliest_possible_start, task.start)]
        dates_owner_utilized = list(task.team_member.calc_utilization_schedule().keys())
        dates_that_could_be_filled = sorted(list(set(dates_in_leading_gap) - set(dates_owner_utilized)))

        # divide the list of dates that could be filled into sub-lists of continuous dates
        min_date = min(dates_that_could_be_filled)
        integer_version = [(date - min_date).days for date in dates_that_could_be_filled]
        continuous_dates = [[min_date + timedelta(x) for x in list(group)]
                            for group in mit.consecutive_groups(integer_version)]

        for group in continuous_dates:
            if len(group) > 0.5 * float(task.baseline_fte_days):  # then shift task forward
                task.set_task_days_forward(group[0] - timedelta(1))
                break


def timeline_utilization(request):
    project = Project.objects.get(id=request.GET['project_id'])

    project.setup_gantt()
    utilization_schedule = create_utilization_schedules(project)
    gantt_data = create_gantt_json(project)

    ajax_data = {
        'gantt_data': gantt_data,
        'utilization_schedule': utilization_schedule
    }
    return JsonResponse(data=json.dumps(ajax_data), safe=False)
