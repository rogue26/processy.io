import io

from django.http import HttpResponse
from django.core.files.base import ContentFile

from docx import Document

from projects.models import ScopeOfWork


def ajax_test(request):
    if request.method == 'GET':
        project_id = request.GET['project_id']

        # buffer = StringIO()
        #
        # document = Document()
        # document.add_heading('Document Title', 0)
        # document.add_paragraph('A plain paragraph having some ')

        # with open('foobar.docx', 'rb') as f:
        #     source_stream = StringIO(f.read())
        # document = Document(source_stream)

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
