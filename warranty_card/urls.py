from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import RegisterView, UserListView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("users/", UserListView.as_view(), name="user-list"),]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)