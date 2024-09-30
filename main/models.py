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
