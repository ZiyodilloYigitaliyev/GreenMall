import os
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A2  # ✅ A2 format kattaroq chiqadi
from reportlab.lib.colors import white

# 📂 PDF va shrift kataloglari
GENERATED_PDF_DIR = os.path.join(settings.MEDIA_ROOT, "generated")
os.makedirs(GENERATED_PDF_DIR, exist_ok=True)

# ✅ Arial shriftini yuklash
FONT_PATH = os.path.join(settings.MEDIA_ROOT, "fonts/arial.ttf")
pdfmetrics.registerFont(TTFont("Arial", FONT_PATH))

# 🎮 Rasm va fon manzillari
LOGO_PATH = os.path.join(settings.MEDIA_ROOT, "images/logo.png")  # Logotip
BACKGROUND_PATH = os.path.join(settings.MEDIA_ROOT, "images/background.png")  # PNG fon rasmi
IMAGE_PATH = os.path.join(settings.MEDIA_ROOT, "images/Group_90.png")  # Foydalanuvchi yuborgan rasm

def generate_user_pdf(user):
    pdf_filename = "warranty_card.pdf"
    output_pdf_path = os.path.join(GENERATED_PDF_DIR, pdf_filename)

    # ✅ PDF yaratamiz (A2 formatda)
    c = canvas.Canvas(output_pdf_path, pagesize=A2)
    page_width, page_height = A2  # A2 sahifa o‘lchami

    # 🎮 RASMNI CHIROYLI JOYLASHTIRISH
    IMAGE_WIDTH = 1200  # ✅ Rasm kengligi
    IMAGE_HEIGHT = 800  # ✅ Rasm balandligi
    X_POSITION = (page_width - IMAGE_WIDTH) / 2  # Markazlash
    Y_POSITION = (page_height - IMAGE_HEIGHT) / 2

    if os.path.exists(IMAGE_PATH):
        c.drawImage(IMAGE_PATH, X_POSITION, Y_POSITION, width=IMAGE_WIDTH, height=IMAGE_HEIGHT, mask='auto')

    # 📈 Foydalanuvchi ma'lumotlarini rasm ustiga yozish
    c.setFont("Arial", 20)  # ✅ Shrifi kattalashtirildi
    c.setFillColor(white)  # Matn rangi oq

    # 📍 Joylashuv koordinatalari
    c.drawString(X_POSITION + 100, Y_POSITION + 700, f"{user.name} {user.surname}")  # F.I.O
    c.drawString(X_POSITION + 100, Y_POSITION + 640, user.address)  # Adres montaja
    c.drawString(X_POSITION + 100, Y_POSITION + 580, user.phone)  # Kontaktnyy nomer
    c.drawString(X_POSITION + 100, Y_POSITION + 520, user.email)  # E-mail

    # ✅ PDF'ni saqlash
    c.showPage()
    c.save()

    return pdf_filename  # 📂 Faqat fayl nomini qaytaradi
