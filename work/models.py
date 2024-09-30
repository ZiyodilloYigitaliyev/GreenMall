from django.db import models


class Project(models.Model):
    title_en = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_uz = models.CharField(max_length=255)

    description_en = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)
    description_uz = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title_uz


class ProjectMedia(models.Model):
    project = models.ForeignKey(Project, related_name='media', on_delete=models.CASCADE)
    file = models.FileField(upload_to='project_media/')

    def __str__(self):
        return f"Media for {self.project.title_uz} - {self.file.name}"
