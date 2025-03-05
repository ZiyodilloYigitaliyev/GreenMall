import os
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black


GENERATED_PDF_DIR = os.path.join(settings.MEDIA_ROOT, "generated")
os.makedirs(GENERATED_PDF_DIR, exist_ok=True)

FONT_PATH = os.path.join(settings.MEDIA_ROOT, "fonts/arial.ttf")
pdfmetrics.registerFont(TTFont("Arial", FONT_PATH))

LOGO_PATH = os.path.join(settings.MEDIA_ROOT, "images/logo.png") 

def generate_user_pdf(user):
    pdf_filename = "warranty_card.pdf"
    output_pdf_path = os.path.join(GENERATED_PDF_DIR, pdf_filename)


    c = canvas.Canvas(output_pdf_path, pagesize=A4)
    c.setFont("Arial", 20)


    page_width, page_height = A4

    logo_width, logo_height = 120, 120  
    logo_x = (page_width - logo_width) / 2  
    logo_y = page_height - logo_height - 20 

    if os.path.exists(LOGO_PATH):
        c.drawImage(LOGO_PATH, logo_x, logo_y, width=logo_width, height=logo_height, mask='auto')

    c.setFillColor(black)
    c.drawCentredString(page_width / 2, logo_y - 30, f"ГАРАНТИЙНЫЙ ТАЛОН N {user.unique_code}")

    c.setFont("Arial", 14)

    left_x = 100
    right_x = 350
    y_position = 620

    c.drawString(left_x, y_position, "💡 F.I.O:")
    c.drawString(right_x, y_position, f"{user.name} {user.surname}")

    c.drawString(left_x, y_position - 30, "📍 Manzil:")
    c.drawString(right_x, y_position - 30, user.address)

    c.drawString(left_x, y_position - 60, "📞 Telefon:")
    c.drawString(right_x, y_position - 60, user.phone)

    c.drawString(left_x, y_position - 90, "✉️ Email:")
    c.drawString(right_x, y_position - 90, user.email)


    c.showPage()
    c.save()

    return pdf_filename
