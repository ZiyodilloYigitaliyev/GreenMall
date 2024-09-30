from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main.views import StatsListView
from work.views import *
from products.views import *
urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/projects/', ProjectListCreateView.as_view(), name='project-list-create'),
        path('api/projects/<int:pk>/', ProjectListCreateView.as_view(), name='project-detail' ),
        path('api/stats/', StatsListView.as_view(), name='stats-list'),
        path('api/products/', ProductListCreateView.as_view(), name='product-list-create'),
        path('api/products/<int:pk>/', ProductListCreateView.as_view(), name='product-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

