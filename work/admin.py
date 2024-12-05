from django.contrib import admin
from .models import Project, ProjectMedia

class ProjectMediaInline(admin.TabularInline):
    model = ProjectMedia
    extra = 1  # Add one extra empty form to add a new media file

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_uz', 'description_uz')
    inlines = [ProjectMediaInline]

@admin.register(ProjectMedia)
class ProjectMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'file_url')
