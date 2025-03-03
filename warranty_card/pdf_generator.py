import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

MEDIA_DIR = "media"

if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

def generate_user_pdf(user):
    filename = f"user_{user.unique_code}.pdf"
    filepath = os.path.join(MEDIA_DIR, filename)

    c = canvas.Canvas(filepath, pagesize=A4)
    c.setFont("Helvetica", 12)

    c.drawString(100, 800, f"ГАРАНТИЙНЫЙ ТАЛОН N. {user.unique_code}")
    c.drawString(100, 780, f"Ф.И.О: {user.name} {user.surname}")
    c.drawString(100, 760, f"Адрес монтажа: {user.address}")
    c.drawString(100, 740, f"Контактный номер: {user.phone}")
    c.drawString(100, 720, f"E-mail: {user.email}")

    c.save()
    return filepath
