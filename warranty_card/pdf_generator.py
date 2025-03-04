import os
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black, blue

GENERATED_PDF_DIR = os.path.join(settings.MEDIA_ROOT, "generated")
os.makedirs(GENERATED_PDF_DIR, exist_ok=True)

FONT_PATH = os.path.join(settings.MEDIA_ROOT, "fonts/arial.ttf")
pdfmetrics.registerFont(TTFont("Arial", FONT_PATH))

def generate_user_pdf(user):
    """
    Foydalanuvchi ma'lumotlari asosida chiroyli PDF yaratish.
    """
    pdf_filename = "ГАРАНТИЙНЫЙ_ТАЛОН.pdf"
    output_pdf_path = os.path.join(GENERATED_PDF_DIR, pdf_filename)

    # ✅ PDF yaratamiz
    c = canvas.Canvas(output_pdf_path, pagesize=A4)

    # 📌 Sarlavha: "ГАРАНТИЙНЫЙ ТАЛОН N 500892"
    c.setFillColor(black)
    c.setFont("Arial", 20)
    c.drawCentredString(300, 820, f"ГАРАНТИЙНЫЙ ТАЛОН N {user.unique_code}")

    # 📌 Foydalanuvchi ma'lumotlari
    c.setFont("Arial", 14)

    c.drawString(100, 700, f"💡 F.I.O: {user.name} {user.surname}")
    c.drawString(100, 670, f"📍 Manzil: {user.address}")
    c.drawString(100, 640, f"📞 Telefon: {user.phone}")
    c.drawString(100, 610, f"✉️ Email: {user.email}")

    # ✅ PDF'ni saqlash
    c.showPage()
    c.save()

    return pdf_filename  # 📂 Faqat fayl nomini qaytaradi
