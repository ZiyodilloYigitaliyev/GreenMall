import os
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black

# 📂 PDF va shrift kataloglari
GENERATED_PDF_DIR = os.path.join(settings.MEDIA_ROOT, "generated")
os.makedirs(GENERATED_PDF_DIR, exist_ok=True)

# ✅ Arial shriftini yuklash
FONT_PATH = os.path.join(settings.MEDIA_ROOT, "fonts/arial.ttf")
pdfmetrics.registerFont(TTFont("Arial", FONT_PATH))

# 🖼️ Rasm va fon manzillari
LOGO_PATH = os.path.join(settings.MEDIA_ROOT, "images/logo.png")  # Logotip joylashuvi
BACKGROUND_PATH = os.path.join(settings.MEDIA_ROOT, "images/background.png")  # PNG fon rasmi

def generate_user_pdf(user):
    pdf_filename = "warranty_card.pdf"
    output_pdf_path = os.path.join(GENERATED_PDF_DIR, pdf_filename)

    # ✅ PDF yaratamiz
    c = canvas.Canvas(output_pdf_path, pagesize=A4)
    page_width, page_height = A4  # Sahifa o‘lchami

    # 🖼️ PNG FON RASMINI JOYLASH (butun sahifa uchun)
    if os.path.exists(BACKGROUND_PATH):
        c.drawImage(BACKGROUND_PATH, 0, 0, width=page_width, height=page_height, mask='auto')

    # 🖼️ Logotipni joylash (eng yuqori markazda)
    logo_width, logo_height = 120, 120  # Logotip o‘lchami
    logo_x = (page_width - logo_width) / 2  # Markazga moslash
    logo_y = page_height - logo_height - 20  # Eng yuqorida joylash (20px bo‘sh joy)

    if os.path.exists(LOGO_PATH):
        c.drawImage(LOGO_PATH, logo_x, logo_y, width=logo_width, height=logo_height, mask='auto')

    # 📌 Sarlavha (Markazda, logotip ostida)
    c.setFont("Arial", 20)
    c.setFillColor(black)
    c.drawCentredString(page_width / 2, logo_y - 30, f"ГАРАНТИЙНЫЙ ТАЛОН N {user.unique_code}")

    # 📌 Foydalanuvchi ma'lumotlari yonma-yon chiqariladi
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

    # ✅ PDF'ni saqlash
    c.showPage()
    c.save()

    return pdf_filename  # 📂 Faqat fayl nomini qaytaradi
