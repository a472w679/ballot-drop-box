import csv

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import imb

# Create your views here.

def home(request):
  template = loader.get_template('home.html')
  context = {
  }
  return HttpResponse(template.render(context, request))

def dashboard(request, dropbox_id):
  envelopeimb_data = imb.objects.all().filter(dropboxid=dropbox_id).values()
  template = loader.get_template('dropbox.html')
  context = {
    'imbdata': envelopeimb_data,
    'dropbox_id': dropbox_id,
  }
  return HttpResponse(template.render(context, request))

def export(request, dropbox_id):  # downloads database in a csv 
    response = HttpResponse(content_type = 'text/csv')
    writer = csv.writer(response)
    writer.writerow(['Dropbox ID', 'Code 39', 'IMb', 'Date', 'Street Address', 'City', 'Zip Code', 'Status'])

    for data in imb.objects.all().filter(dropboxid=dropbox_id).values_list('dropboxid', 'imb', 'code39', 'date', 'streetaddress', 'city', 'zipcode', 'status'): 
        writer.writerow(data)

    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    return response 



