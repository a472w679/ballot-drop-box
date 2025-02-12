import csv

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

def export(request):  # downloads database in a csv 
    response = HttpResponse(content_type = 'text/csv')
    writer = csv.writer(response)
    writer.writerow(['Dropbox ID', 'Code 39', 'IMb', 'Date', 'Street Address', 'City', 'Zip Code', 'Status'])

    for data in imb.objects.all().values_list('dropboxid', 'imb', 'code39', 'date', 'streetaddress', 'city', 'zipcode', 'status'): 
        writer.writerow(data)

    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    return response 



