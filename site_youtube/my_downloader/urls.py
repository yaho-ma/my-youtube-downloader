from django.urls import path
from . import views

app_name = 'YT-downloader'


urlpatterns = [
    path('', views.index_view),
    path('download/', views.download_view),
    path('download/<res>/', views.success, name="success"),
]
