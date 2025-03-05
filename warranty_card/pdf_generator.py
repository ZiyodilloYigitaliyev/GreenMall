import os
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
    pdf_filename = "document.pdf"
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
    c.drawCentredString(page_width / 2, page_height - 150, "Kafolat Kartasi")  # **Sarlavha** (Warranty Card)

    # 📝 Asosiy ma'lumotlar
    c.setFont("Arial", 14)

    text_lines = [
        f"F.I.O: {user.name} {user.surname}",
        f"Adres: {user.address}",
        f"Telefon: {user.phone}",
        f"E-mail: {user.email}",
        "Kafolat muddati: 12 oy",
        "Izoh: Ushbu hujjat mahsulotning kafolatli ekanligini tasdiqlaydi.",
        "Iltimos, kafolatni saqlang va kerak bo‘lsa biz bilan bog‘laning."
    ]

    x_text = 100
    y_text = page_height - 200  # Logotipdan pastroq

    for line in text_lines:
        c.drawString(x_text, y_text, line)
        y_text -= 30  # Har bir qatorni pastga suramiz

    # ✅ PDF'ni saqlash
    c.showPage()
    c.save()

    return pdf_filename  # 📂 Faqat fayl nomini qaytaradi
