from django.db import models
from django.core.exceptions import ValidationError


class Stats(models.Model):
    years_in_market = models.PositiveIntegerField(default=0, verbose_name="Yillar bozorda")
    satisfied_clients = models.PositiveIntegerField(default=0, verbose_name="Mamnun mijozlar")
    installed_items_km = models.FloatField(default=0, verbose_name="O'rnatilgan panjaralar (km)")
    work_all_days = models.PositiveIntegerField(default=0, verbose_name="Ish kunlari minimal")

    def clean(self):
        if Stats.objects.exists() and not self.pk:
            raise ValidationError("Faqat bitta statistika ma'lumotini saqlash mumkin.")
    def __str__(self):
        return f"{self.years_in_market} years in market, {self.satisfied_clients} satisfied clients"


class Order(models.Model):
    first_name = models.CharField(max_length=50)  # Ism
    last_name = models.CharField(max_length=50)   # Familya
    phone_number = models.CharField(max_length=15)  # Telefon raqami
    product_length = models.DecimalField(max_digits=5, decimal_places=2)  # Mahsulot bo'yi
    product_width = models.DecimalField(max_digits=5, decimal_places=2)   # Mahsulot eni
    product_area = models.DecimalField(max_digits=8, decimal_places=2)    # Mahsulot yuzasi
    description = models.TextField(blank=True)  # Qo'shimcha ma'lumotlar
    date = models.DateField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)  # Buyurtma tekshirilganmi yoki yo'qmi

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.phone_number}"
