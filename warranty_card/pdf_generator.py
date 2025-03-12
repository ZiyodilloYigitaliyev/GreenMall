import os
import uuid
import boto3
import datetime
from io import BytesIO
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black
from PIL import Image, ImageDraw, ImageFont
import requests

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION_NAME,
)




AWS_BASE_URL = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}"

FONT_PATH = os.path.join(settings.MEDIA_ROOT, "fonts/arial.ttf")
pdfmetrics.registerFont(TTFont("Arial", FONT_PATH))

IMAGE_URL = f"{AWS_BASE_URL}/images/Frame_27.jpg"

# 📌 1️⃣ **AWS S3'dan rasmni yuklash**
def download_image_from_s3(image_url):
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content)).convert("RGB")  # ✅ JPG formatida o‘qish
    else:
        raise Exception(f"Rasm yuklab olinmadi: {image_url}")

# 📌 2️⃣ **Matnni rasmga joylashtirish**
def add_text_to_image(image, text_data, special_text=None):
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype(FONT_PATH, 50)  # **Shrift 50px**
    except IOError:
        font = ImageFont.load_default()

    special_text = special_text or {}

    for text, (x, y) in text_data.items():
        color = "#0C4840" if text in special_text else "white"  # ✅ **Oq emas, qora rang ishlatiladi**
        draw.text((x, y), text, fill=color, font=font)

    return image

# 📌 3️⃣ **Rasmni PDF formatiga o‘tkazish**
def convert_image_to_pdf(image):
    pdf_bytes = BytesIO()
    image.save(pdf_bytes, format="PDF")  # ✅ **Pillow yordamida JPG dan to‘g‘ri PDF yaratish**
    return pdf_bytes.getvalue()

# 📌 4️⃣ **Foydalanuvchi uchun PDF yaratish va S3'ga yuklash**
def generate_user_pdf(user):
    unique_code = str(uuid.uuid4())[:8]
    pdf_filename = f"warranty_card_{unique_code}.pdf"

    # 📆 **Bugungi sana avtomatik**
    today_date = datetime.datetime.now().strftime("%d.%m.%Y")
    
    # ✅ **Matn koordinatalari**
    text_data = {
        user.surname: (210, 1480),
        user.name: (1390, 1480),
        user.address: (210, 1835),
        user.phone: (1390, 1850),
        today_date: (1450, 1100), 
        "100": (1840, 1100),
        unique_code: (1550, 830),
    }


    # 🔴 **Qizil rangda chiqariladigan matnlar**
    special_text = {unique_code}

    # 📍 1️⃣ **AWS S3'dan rasmni yuklash (JPG)**
    image = download_image_from_s3(IMAGE_URL)

    # 📍 2️⃣ **Rasmga foydalanuvchi ma’lumotlarini joylashtirish**
    filled_image = add_text_to_image(image, text_data, special_text)

    # 📍 3️⃣ **JPG'ni PDF formatiga o‘tkazish**
    pdf_content = convert_image_to_pdf(filled_image)

    # 📤 4️⃣ **AWS S3'ga yuklash**
    s3_key = f"generated/{pdf_filename}"
    s3_client.put_object(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=s3_key,
        Body=pdf_content,
        ContentType="application/pdf",
    )

    # 🌐 5️⃣ **S3'dagi PDF fayl URL'si**
    pdf_url = f"{settings.AWS_S3_CUSTOM_DOMAIN}/{s3_key}"

    return pdf_url
