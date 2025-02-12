from django.urls import path

from . import views

urlpatterns = [
    path('envelopeimb/', views.envelopeimb, name='envelopeimb'),
    path('export/', views.export, name='export'),
    path('', views.envelopeimb, name='envelopeimb'),
]
