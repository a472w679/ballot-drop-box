from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('dashboard/<int:dropbox_id>', views.dashboard, name='dashboard'),
    path('list/', views.dropbox_list, name='list'),
    path('export/<int:dropbox_id>', views.export, name='export'),
    path('api/scandata', views.receive_sensor_data, name='receive_sensor_data'),
    path('videos/<str:video_filename>', views.video, name='video'),
    path('video-list/', views.video_list, name='video-list'),
    path('map', views.map, name='map'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('account/', views.account, name='account'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
