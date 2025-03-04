import os
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4

TEMPLATE_PDF = "media/templates/Frame_25.pdf"
FONT_PATH = "media/fonts/arial.ttf"
GENERATED_PDF_DIR = "media/generated"

os.makedirs(GENERATED_PDF_DIR, exist_ok=True)

pdfmetrics.registerFont(TTFont("Arial", FONT_PATH))

def generate_user_pdf(user):
    output_pdf_path = os.path.join(GENERATED_PDF_DIR, f"{user.unique_code}.pdf")

    existing_pdf = PdfReader(TEMPLATE_PDF)
    output_pdf = PdfWriter()
    
    temp_pdf_path = "temp.pdf"
    c = canvas.Canvas(temp_pdf_path, pagesize=A4)
    c.setFont("Arial", 12)


    c.drawString(420, 640, f"{user.unique_code}") 
    c.drawString(140, 580, f"{user.name} {user.surname}") 
    c.drawString(140, 550, f"{user.address}")  
    c.drawString(140, 520, f"{user.phone}") 
    c.drawString(140, 490, f"{user.email}") 
    
    c.save()

    temp_pdf = PdfReader(temp_pdf_path)
    first_page = existing_pdf.pages[0]
    first_page.merge_page(temp_pdf.pages[0])
    output_pdf.add_page(first_page)

    with open(output_pdf_path, "wb") as output_file:
        output_pdf.write(output_file)


    os.remove(temp_pdf_path)

    return output_pdf_path
