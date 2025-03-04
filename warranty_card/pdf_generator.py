import os
from django.conf import settings
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4

TEMPLATE_PDF = os.path.join(settings.MEDIA_ROOT, "templates/Frame_25.pdf")
FONT_PATH = os.path.join(settings.MEDIA_ROOT, "fonts/arial.ttf")
GENERATED_PDF_DIR = os.path.join(settings.MEDIA_ROOT, "generated")

os.makedirs(GENERATED_PDF_DIR, exist_ok=True)

pdfmetrics.registerFont(TTFont("Arial", FONT_PATH))

def generate_user_pdf(user):
    """
    Foydalanuvchi ma'lumotlari bilan PDF yaratish.
    """
    pdf_filename = f"{user.unique_code}.pdf"
    output_pdf_path = os.path.join(GENERATED_PDF_DIR, pdf_filename)

    existing_pdf = PdfReader(TEMPLATE_PDF)
    output_pdf = PdfWriter()

    temp_pdf_path = os.path.join(settings.MEDIA_ROOT, "temp.pdf")
    c = canvas.Canvas(temp_pdf_path, pagesize=A4)
    c.setFont("Arial", 14)

    c.drawString(420, 640, f"{user.unique_code}")  
    c.drawString(140, 580, f"{user.name} {user.surname}") 
    c.drawString(140, 550, f"{user.address}")  
    c.drawString(140, 520, f"{user.phone}")  
    c.drawString(140, 490, f"{user.email}")  

    c.showPage()
    c.save()

    temp_pdf = PdfReader(temp_pdf_path)
    output_pdf.add_page(existing_pdf.pages[0])  
    output_pdf.pages[0].merge_page(temp_pdf.pages[0]) 

    with open(output_pdf_path, "wb") as output_file:
        output_pdf.write(output_file)

    os.remove(temp_pdf_path)

    return pdf_filename 
