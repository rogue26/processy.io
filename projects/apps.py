from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    name = 'projects'

    # todo: this stopped working after moving to postgresql - may just need to create a reference project first...
    # def ready(self):
    #     from .models import Project
    #
    #     try:
    #         if not Project.objects.all().exists():
    #             Project.objects.create(name='Reference project',
    #                                    description='Dummy project to contain all workstreams, deliverables, '
    #                                                'and tasks that will be used as sensible defaults',
    #                                    cluster="N/A",
    #                                    client="N/A",
    #                                    is_the_reference_project=True
    #                                    )
    #     except django.db.utils.OperationalError:
    #         pass
