import os
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A3
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

    # ✅ PDF yaratamiz
    c = canvas.Canvas(output_pdf_path, pagesize=A3)
    page_width, page_height = A3  # Sahifa o‘lchami (A3, landshaft rejimida)

    # 🎮 PNG FON RASMINI JOYLASH (butun sahifa uchun)
    if os.path.exists(IMAGE_PATH):
        c.drawImage(IMAGE_PATH, 0, 0, width=page_width, height=page_height, mask='auto')

    # 📈 Foydalanuvchi ma'lumotlarini rasm ustiga yozish
    c.setFont("Arial", 16)
    c.setFillColor(white)  # Matn rangi oq

    # Joylashuv koordinatalari (rasmga mos ravishda)
    c.drawString(300, 700, f"{user.name} {user.surname}")  # F.I.O
    c.drawString(300, 640, user.address)  # Adres montaja
    c.drawString(300, 580, user.phone)  # Kontaktnyy nomer
    c.drawString(300, 520, user.email)  # E-mail

    # ✅ PDF'ni saqlash
    c.showPage()
    c.save()

    return pdf_filename  # 📂 Faqat fayl nomini qaytaradi
