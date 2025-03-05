import os
import uuid
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4  # 📄 Hujjat rasmi A4 formatda bo‘ladi
from reportlab.lib.colors import black

# 📂 PDF fayllar uchun katalog
GENERATED_PDF_DIR = os.path.join(settings.MEDIA_ROOT, "generated")
os.makedirs(GENERATED_PDF_DIR, exist_ok=True)

# ✅ Arial shriftini yuklash
FONT_PATH = os.path.join(settings.MEDIA_ROOT, "fonts/arial.ttf")
pdfmetrics.registerFont(TTFont("Arial", FONT_PATH))

# 🎯 Logotip uchun fayl
LOGO_PATH = os.path.join(settings.MEDIA_ROOT, "images/logo.png")

def generate_user_pdf(user):
    unique_code = str(uuid.uuid4())[:8]  # 📌 8 ta belgili unikal kod yaratamiz
    pdf_filename = f"warranty_card_{unique_code}.pdf"
    output_pdf_path = os.path.join(GENERATED_PDF_DIR, pdf_filename)

    # 📄 PDF yaratamiz (A4 formatda)
    c = canvas.Canvas(output_pdf_path, pagesize=A4)
    page_width, page_height = A4  # Sahifa o‘lchami

    # 🏢 Logotip joylashuvi
    if os.path.exists(LOGO_PATH):
        LOGO_WIDTH = 150
        LOGO_HEIGHT = 50
        LOGO_X = (page_width - LOGO_WIDTH) / 2  # Markazda joylash
        LOGO_Y = page_height - 100
        c.drawImage(LOGO_PATH, LOGO_X, LOGO_Y, width=LOGO_WIDTH, height=LOGO_HEIGHT, mask='auto')

    # 📃 Hujjat sarlavhasi
    c.setFont("Arial", 18)
    c.setFillColor(black)
    c.drawCentredString(page_width / 2, page_height - 150, f"Kafolat Kartasi N_{unique_code}")  # **Sarlavha** (Warranty Card)

    # 📝 Ma'lumotlar bitta qatorda bo‘lishi kerak
    c.setFont("Arial", 14)

    user_data = f"F.I.O: {user.name} {user.surname}  ||  Adres: {user.address}  ||  Telefon: {user.phone}  ||  E-mail: {user.email}"
    
    x_text = 50
    y_text = page_height - 200  # Logotipdan pastroq
    max_width = page_width - 100  # Matn sahifa chegaralariga chiqmasligi uchun

    # 📌 Agar matn uzun bo‘lsa, avtomatik ravishda ikkita qatorga ajratamiz
    if c.stringWidth(user_data, "Arial", 14) > max_width:
        parts = user_data.split("  ||  ")
        line1 = "  ||  ".join(parts[:2])  # Birinchi yarim qismi
        line2 = "  ||  ".join(parts[2:])  # Ikkinchi yarim qismi
        c.drawString(x_text, y_text, line1)
        c.drawString(x_text, y_text - 30, line2)
    else:
        c.drawString(x_text, y_text, user_data)

    # ✅ PDF'ni saqlash
    c.showPage()
    c.save()

    return pdf_filename  # 📂 Faqat fayl nomini qaytaradi
