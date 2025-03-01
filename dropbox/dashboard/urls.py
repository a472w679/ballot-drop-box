from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='dashboard'),
    path('dashboard/<int:dropbox_id>', views.dashboard, name='dashboard'),
    path('export/<int:dropbox_id>', views.export, name='export'),
]
