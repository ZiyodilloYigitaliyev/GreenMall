import os
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import white

# 📂 PDF va shrift kataloglari
GENERATED_PDF_DIR = os.path.join(settings.MEDIA_ROOT, "generated")
os.makedirs(GENERATED_PDF_DIR, exist_ok=True)

# ✅ Arial shriftini yuklash
FONT_PATH = os.path.join(settings.MEDIA_ROOT, "fonts/arial.ttf")
pdfmetrics.registerFont(TTFont("Arial", FONT_PATH))

# 🖼️ Rasm va fon manzillari
LOGO_PATH = os.path.join(settings.MEDIA_ROOT, "images/logo.png")  # Logotip
BACKGROUND_PATH = os.path.join(settings.MEDIA_ROOT, "images/background.png")  # PNG fon rasmi
TEMPLATE_IMAGE_PATH = os.path.join(settings.MEDIA_ROOT, "images/Group_90.png")  # Yangi rasm

def generate_user_pdf(user):
    pdf_filename = "warranty_card.pdf"
    output_pdf_path = os.path.join(GENERATED_PDF_DIR, pdf_filename)

    # ✅ PDF yaratamiz
    c = canvas.Canvas(output_pdf_path, pagesize=A4)
    page_width, page_height = A4  # Sahifa o‘lchami

    # 🖼️ PNG FON RASMINI JOYLASH (butun sahifa uchun)
    if os.path.exists(BACKGROUND_PATH):
        c.drawImage(BACKGROUND_PATH, 0, 0, width=page_width, height=page_height, mask='auto')

    # 🖼️ Yangi rasmni joylash
    if os.path.exists(TEMPLATE_IMAGE_PATH):
        c.drawImage(TEMPLATE_IMAGE_PATH, 50, 400, width=500, height=150, mask='auto')

    # 🖼️ Logotipni joylash (eng yuqori markazda)
    logo_width, logo_height = 120, 120  # Logotip o‘lchami
    logo_x = (page_width - logo_width) / 2  # Markazga moslash
    logo_y = page_height - logo_height - 20  # Eng yuqorida joylash (20px bo‘sh joy)

    if os.path.exists(LOGO_PATH):
        c.drawImage(LOGO_PATH, logo_x, logo_y, width=logo_width, height=logo_height, mask='auto')

    # 📌 Sarlavha (Markazda, logotip ostida)
    c.setFont("Arial", 20)
    c.setFillColor(white)  # ✅ Matn rangi oq rangga o‘zgartirildi
    c.drawCentredString(page_width / 2, logo_y - 30, f"ГАРАНТИЙНЫЙ ТАЛОН N_{user.unique_code}")

    # 📌 Foydalanuvchi ma'lumotlarini rasm joylashuviga mos yozish
    c.setFont("Arial", 14)
    y_position = 475  # Rasm ustidagi boshlang'ich balandlik
    line_spacing = 30  # Har bir yozuv orasidagi masofa

    labels = ["F.I.O:", "Adres montaja:", "Kontaktnyy nomer:", "E-mail:"]
    values = [f"{user.name} {user.surname}", user.address, user.phone, user.email]

    for i in range(len(labels)):
        c.drawString(70, y_position - (i * line_spacing), labels[i])
        c.drawString(220, y_position - (i * line_spacing), values[i])  # Yonma-yon chiqarish

    # ✅ PDF'ni saqlash
    c.showPage()
    c.save()

    return pdf_filename  # 📂 Faqat fayl nomini qaytaradi
