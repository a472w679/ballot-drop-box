# Name of code artifact: views.py 
# Brief description of what the code does: Routes different templates depending on url 
# Programmer’s name: Xavier Ruyle 
# Date the code was created: 2/20/25 
# Preconditions: database available 
# Postconditions: N/A 
# Return values or types, and their meanings: N/A 
# Error and exception condition values or types that can occur, and their meanings: N/A 
# Side effects: 
# Invariants: N/A 

import csv
import datetime
import os

import numpy as np
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from rest_framework import status
# rest-api
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import EnvelopeScan
from .serializers import EnvelopeSerializer

# Create your views here.

def home(request):
  template = loader.get_template('home.html')
  context = {
  }
  return HttpResponse(template.render(context, request))

def dashboard(request, dropbox_id):
  envelope_data = EnvelopeScan.objects.all().filter(dropboxid=dropbox_id).values()

  # getting media files from static/media 
  media_files = []
  media_dir = os.path.join(os.path.dirname(__file__), 'media')
  for filename in os.listdir(media_dir): 
    if filename.endswith('.webm') and filename.startswith(str(dropbox_id)): 
            full_path = os.path.join(media_dir, filename)
            time = os.path.getmtime(full_path)
            size = str(round(os.path.getsize(full_path) / (1024 * 1024), 2)) + " MB"
            datetime_object = datetime.datetime.fromtimestamp(time)
            formatted_time = datetime_object.strftime("%Y-%m-%d %H:%M:%S")

            media_files.append((filename, size, formatted_time)) 

  template = loader.get_template('dropbox.html')
  context = {
    'envelope_data': envelope_data,
    'dropbox_id': dropbox_id,
    'media_files': media_files
  }
  return HttpResponse(template.render(context, request))

def video(request, video_filename): 
    template = loader.get_template('video.html')

    context = {
        'video_filename': video_filename,
        'path': f'{settings.MEDIA_URL}{video_filename}'
    }
    return HttpResponse(template.render(context, request))

def export(request, dropbox_id):  # downloads database in a csv 
    response = HttpResponse(content_type = 'text/csv')
    writer = csv.writer(response)
    writer.writerow(['Dropbox ID', 'Code 39', 'IMb', 'Date', 'Street Address', 'City', 'Zip Code', 'Status'])

    for data in EnvelopeScan.objects.all().filter(dropboxid=dropbox_id).values_list('dropboxid', 'imb', 'code39', 'date', 'streetaddress', 'city', 'zipcode', 'status'): 
        writer.writerow(data)

    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    return response 

@api_view(['POST'])
def receive_sensor_data(request):
    serializer = EnvelopeSerializer(data=request.data)
    if serializer.is_valid(): # makes sure post request is valid 
        serializer.save() # inserts data 
        res = Response(serializer.data, status=status.HTTP_201_CREATED)  

        return res

    res = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return res


