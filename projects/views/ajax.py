import io
import datetime

from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.shortcuts import render
from docx import Document

from projects.models import ScopeOfWork, Project


def project_scope_details():
    pass


def project_approach_details():
    pass


def project_deliverables_details():
    pass


def project_team_details():
    pass


def project_investment_details():
    pass


def ajax_test(request):
    if request.method == 'GET':
        project_id = request.GET['project_id']

        project = Project.objects.get(id=project_id)

        replace_dict = \
            {
                # "organization_name": project.organization.name,
                # "organization_address": project.organization.address,
                # "client_name": project.client.name,
                # "client_description": project.client.description,
                # "client_address": project.client.address,
                # "client_nickname": project.client.nickname(),
                # "project_name": project.name,
                # "today_date": datetime.date.today(),
                # "project_objectives": None,  # loop through each workstream objective as bullet point
                # "regional_scope": None,
                # "product_scope": None,
                # "business_unit_scope": None,
                # "channel_scope": None,

            }

        document = Document()
        document.add_heading('Document Title', 0)
        document.add_paragraph('A plain paragraph having some ')

        # Create in-memory buffer
        file_stream = io.BytesIO()
        # Save the .docx to the buffer
        document.save(file_stream)
        # Reset the buffer's file-pointer to the beginning of the file
        file_stream.seek(0)

        document.save(file_stream)

        # word_file = ContentFile(file_stream.getvalue().encode('utf-8'))
        word_file = ContentFile(file_stream.getvalue())
        # source_stream.close()

        # target_stream = StringIO()
        # document.save(target_stream)

        # row = ["Project ID", project_id]
        # buffer = StringIO()
        # csv_writer = csv.writer(buffer)
        # csv_writer.writerow(row)
        # csv_file = ContentFile(buffer.getvalue().encode('utf-8'))
        sow = ScopeOfWork()
        # sow.file.save('output.csv', csv_file)
        sow.file.save('output.docx', word_file)
        sow.save()
        return HttpResponse(sow.file.url)
    else:
        return HttpResponse("unsuccesful")
