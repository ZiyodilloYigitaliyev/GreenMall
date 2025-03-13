from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)