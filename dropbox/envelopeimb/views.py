from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import imb

# Create your views here.

def envelopeimb(request):
  envelopeimb_data = imb.objects.all().values()
  template = loader.get_template('base.html')
  context = {
    'imbdata': envelopeimb_data,
  }
  return HttpResponse(template.render(context, request))

