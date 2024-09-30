from django.db import models


class Product(models.Model):
    title_en = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_uz = models.CharField(max_length=255)
    description_en = models.TextField()
    description_ru = models.TextField()
    description_uz = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()

    def __str__(self):
        return self.title_uz


class ProductMedia(models.Model):
    product = models.ForeignKey(Product, related_name='media', on_delete=models.CASCADE)
    file = models.FileField(upload_to='project_media/')

    def __str__(self):
        return f"Media for {self.product.title_uz} - {self.file.name}"
