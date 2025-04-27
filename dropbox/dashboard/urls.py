from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework.authtoken import views

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('dashboard/<int:dropbox_id>', views.dashboard, name='dashboard'),
    path('list/', views.dropbox_list, name='list'),
    path('export/<int:dropbox_id>/', views.export, name='export'),
    path('export_email/<int:dropbox_id>/', views.export_email, name='export_email'),
    path('api/scandata', views.receive_sensor_data, name='receive_sensor_data'),
    path('videos/<str:video_filename>', views.video, name='video'),
    path('video-list/', views.video_list, name='video-list'),
    path('map', views.map, name='map'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', views.account_login, name='login'),
    path('accounts/logout/', views.account_logout, name='logout'),
    path('accounts/', views.accounts, name='accounts'),
    path('create-dropbox/', views.create_dropbox, name='create_dropbox'),
    path('delete-dropbox/<int:dropbox_id>', views.delete_dropbox, name='delete_dropbox'),
    path('api-token-auth/<str:username>', views.obtain_auth_token, name='obtain_auth_token'),

    path('404/', views.handler404, name='notfound'),
    path('500/', views.handler500, name='servererror'),
    path('403/', views.handler403, name='servererror')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
