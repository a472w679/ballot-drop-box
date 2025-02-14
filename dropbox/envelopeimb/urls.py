from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='envelopeimb'),
    path('dashboard/<int:dropbox_id>', views.dashboard, name='envelopeimb'),
    path('export/<int:dropbox_id>', views.export, name='export'),
]
