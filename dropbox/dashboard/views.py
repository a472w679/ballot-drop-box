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
import os
from datetime import datetime, timedelta

import numpy as np
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count
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
  context = {}
  return HttpResponse(template.render(context, request))

def map(request):
  template = loader.get_template('map.html')
  context = {}
  return HttpResponse(template.render(context, request))

def dropbox_list(request):
  template = loader.get_template('dropbox_list.html')
  unique_dropbox_ids = EnvelopeScan.objects.order_by('dropboxid').values_list('dropboxid', flat=True).distinct()
  context = {"dropbox_ids": unique_dropbox_ids}
  return HttpResponse(template.render(context, request))

def video_list(request): 
  template = loader.get_template('video_list.html')

  # getting media files from static/media 
  media_files = []
  media_dir = os.path.join(os.path.dirname(__file__), 'media')
  for filename in os.listdir(media_dir): 
    if filename.endswith('.webm'): 
            full_path = os.path.join(media_dir, filename)
            time = os.path.getmtime(full_path)
            size = str(round(os.path.getsize(full_path) / (1024 * 1024), 2)) + " MB"
            datetime_object = datetime.fromtimestamp(time)
            formatted_time = datetime_object.strftime("%Y-%m-%d %H:%M:%S")

            media_files.append((filename, size, formatted_time)) 


    context = {"media_files": media_files}
  return HttpResponse(template.render(context, request))

def dashboard(request, dropbox_id):
  filter_by = request.GET.get('filter') 
  if not filter_by: 
        filter_by = '-date'
  
  envelope_data = EnvelopeScan.objects.all().filter(dropboxid=dropbox_id).order_by(f'{filter_by}')

  num_scanned = len(envelope_data)
  media_dir = os.path.join(os.path.dirname(__file__), 'media')
  num_motion_detections = len([x for x in os.listdir(media_dir) if x.endswith(".webm") and x.startswith(f"{dropbox_id}")])


  paginator = Paginator(envelope_data, 10)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  date_labels = [
        (datetime.now() - timedelta(days=i)).strftime('%a') 
        for i in range(6, -1, -1)
    ]
    
  target_dates = [
        (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') 
        for i in range(6, -1, -1)
    ]
    
    # Query ballot counts
  daily_counts = (
        EnvelopeScan.objects
        .filter(dropboxid=dropbox_id, date__in=target_dates)
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )
    
    # Convert to { '2024-04-01': 15, ... } format
  count_dict = {entry['date']: entry['count'] for entry in daily_counts}
    
  series_data = [{
        'x': (datetime.strptime(target_date, '%Y-%m-%d')).strftime('%b %d'),
        'y': count_dict.get(target_date, 0)
    } for day_label, target_date in zip(date_labels, target_dates)]

  template = loader.get_template('dropbox.html')
  context = {
    'num_scanned': num_scanned,
    'num_motion_detections': num_motion_detections,
    'page_obj': page_obj,
    'dropbox_id': dropbox_id,
    'filter_type': filter_by,
    'chart_series': [{
            'name': 'Envelopes Submitted',
            'color': '#1A56DB',
            'data': series_data
        }],
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


