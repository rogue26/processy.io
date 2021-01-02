from django.shortcuts import render
from django.db.models import Sum
from django.http import JsonResponse
from projects.models import Project
from datetime import timedelta
from teams.models import TeamMember


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def create_utilization_schedules(project):
    team_members = TeamMember.objects.filter(project=project)

    project_dates = [date for date in daterange(project.start, project.end)]

    utilization_schedules = []
    for team_member in team_members:
        utizilized_days = team_member.calc_utilization_schedule()
        utilization_schedule = [utizilized_days[date] if date in project_dates else 0 for date in project_dates]
        tm_data = {'labels': project_dates, 'data': utilization_schedule, }
        utilization_schedules.append(tm_data)

    return utilization_schedules


def utilization_chart(request):
    project = Project.objects.get(id=request.GET['project_id'])
    utilization_schedule = create_utilization_schedules(project)
    return JsonResponse(data=utilization_schedule, safe=False)
