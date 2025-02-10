from django.urls import path

from . import views

urlpatterns = [
    path('envelopeimb/', views.envelopeimb, name='envelopeimb'),
    path('', views.envelopeimb, name='envelopeimb'),
]
