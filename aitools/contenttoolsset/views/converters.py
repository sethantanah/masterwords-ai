import io
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from PyPDF2 import PdfReader
from docx import Document


class UploadPDFView(View):
    def get(self, request):
        context = {
            'loaded': False
        }
        return render(request, 'upload_pdf.html', context)

    def post(self, request):
        # Get the uploaded PDF file from the request
        pdf_file = request.FILES.get('file')

        if pdf_file:
            pdf_reader = PdfReader(io.BytesIO(pdf_file.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()

            request.session['extracted_text'] = text
            context = {
                'text': text,
                'loaded': True
            }
            return render(request, 'upload_pdf.html', context)


def download_word(request):
    # get the extracted text from session
    extracted_text = request.session.get('extracted_text', '')
    # create a new Word document
    document = Document()

    # add the extracted text to the document
    document.add_paragraph(extracted_text)

    # create a file-like buffer to receive PDF data
    buffer = io.BytesIO()

    # save the Word document to the buffer
    document.save(buffer)

    # seek to the beginning of the buffer
    buffer.seek(0)

    # set the content type and headers for the response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=extracted_text.docx'

    # create a FileResponse object and return it as the response
    response.write(buffer.read())
    return response
