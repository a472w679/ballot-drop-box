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
from io import StringIO
from pathlib import Path

import numpy as np
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models.functions import JSONObject
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
# rest-api
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .forms import AccountLogin, AccountRegister, DropboxCreate
from .models import Dropbox, EnvelopeScan
from .serializers import DropboxSerializer, EnvelopeSerializer

# Create your views here.

def home(request):
  template = loader.get_template('home.html')
  context = {}
  return HttpResponse(template.render(context, request))

@login_required
def map(request):
  template = loader.get_template('map.html')
  dropboxes = Dropbox.objects.order_by('dropboxid') 
  context = {"dropboxes": dropboxes}
  return HttpResponse(template.render(context, request))

@login_required
def dropbox_list(request):
  template = loader.get_template('dropbox_list.html')
  # unique_dropbox_ids = EnvelopeScan.objects.order_by('dropboxid').values_list('dropboxid', flat=True).distinct()
  dropboxes = Dropbox.objects.order_by('dropboxid') 
  context = {"dropboxes": dropboxes}
  return HttpResponse(template.render(context, request))

@login_required
def video_list(request): 
  template = loader.get_template('video_list.html')

  # getting media files from static/media 
  media_files = []
  media_dir = os.path.join(Path(__file__).resolve().parent.parent, "media")
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

@login_required
def dashboard(request, dropbox_id):
  filter_by = request.GET.get('filter') 

  # to avoid sql injection  
  accepted_filters = {
        '-date', 
        'date', 
        'code39', 
        '-code39'
  }

  if filter_by not in accepted_filters: 
        filter_by = '-date'
  
  envelope_data = EnvelopeScan.objects.all().filter(dropboxid=dropbox_id).order_by(f'{filter_by}')

  num_scanned = len(envelope_data)
  media_dir = os.path.join(Path(__file__).resolve().parent.parent, "media") 


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
  dropbox = Dropbox.objects.get(dropboxid=dropbox_id)  

  context = {
    'dropbox_name': dropbox.location_name,
    'num_scanned': num_scanned,
    'num_motion_detections': num_motion_detections,
    'page_obj': page_obj,
    'dropbox_id': dropbox_id,
    'filter_type': filter_by,
    'chart_series': [{
            'name': 'Envelopes Scanned',
            'data': series_data
        }],
  }

  return HttpResponse(template.render(context, request))

@login_required
def export_email(request, dropbox_id):
    # 1) Build CSV in‑memory
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow([
        'Dropbox ID', 'Code 39', 'IMb',
        'Date', 'Street Address', 'City',
        'Zip Code', 'Status'
    ])

    # ← define qs here
    qs = EnvelopeScan.objects.filter(dropboxid=dropbox_id)
    for row in qs.values_list(
        'dropboxid','code39','imb',
        'date','streetaddress','city',
        'zipcode','status'
    ):
        writer.writerow(row)

    # 2) Prepare subject/addresses
    subject = f"Your Dropbox #{dropbox_id} CSV Export"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [request.user.email]

    # 3) Plain‑text fallback
    text_content = (
        f"Hi {request.user.username},\n\n"
        f"Your CSV export for Dropbox #{dropbox_id} is attached.\n\n"
        "Thanks,\nBallot Dropbox Team"
    )

    # 4) HTML version
    html_content = render_to_string(
        "emails/export_csv.html",
        {
            "user": request.user,
            "dropbox_id": dropbox_id,
            "dashboard_url": request.build_absolute_uri(
                reverse("dashboard", args=[dropbox_id])
            ),
        }
    )

    # 5) Build & send multipart email
    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.attach(f"dropbox_{dropbox_id}.csv", buffer.getvalue(), "text/csv")
    email.send(fail_silently=False)

    messages.success(request, f"CSV emailed to {request.user.email}")
    return redirect("dashboard", dropbox_id=dropbox_id)
    
def video(request, video_filename): 
    template = loader.get_template('video.html')

    context = {
        'video_filename': video_filename,
        'path': f'{settings.MEDIA_URL}{video_filename}'
    }
    return HttpResponse(template.render(context, request))

def account_login(request):
    context = {
        "error_message": "" 
    }

    access_rejected = request.GET.get("next")
    if access_rejected:  # the user tried to access login required pages 
        context["error_message"] = "Login or register to access that page"

    if request.method == 'POST': 
        form = AccountLogin(request.POST)
        if form.is_valid(): 
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user_authenticated = authenticate(username=username, email=email, password=password)
            print(username, email, password, user_authenticated) 
            if user_authenticated:
                login(request, user_authenticated)  # creates session
                return HttpResponseRedirect("/home/")
            else: 
                context["error_message"] = "Account information incorrect!"

    else: 
        form = AccountLogin()

    template = loader.get_template('login.html')
    return HttpResponse(template.render(context, request))

@login_required
def register(request): 
    context = {
        "error_message": "" ,
        "success_message": "" 
    }

    access_rejected = request.GET.get("next")
    if access_rejected:  # the user tried to access login required pages 
        context["error_message"] = "Login or register to access that page"

    template = loader.get_template('register.html')
    if request.method == 'POST': 
        form = AccountRegister(request.POST)
        if form.is_valid(): 
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            confirm_password = form.cleaned_data["confirm_password"]

            if password == confirm_password: 
                user_exists = User.objects.filter(username=username).exists()
                email_exists = User.objects.filter(email=email).exists()
                if user_exists or email_exists: 
                    context["error_message"] = "User already exists with those credentials"
                else: 
                    user = User.objects.create_user(username=username, email=email, password=password) # save user to database 
                    context["success_message"] = "Account created successfully"
            else: 
                context["error_message"] = "Passwords do not match!"
    else: 
        form = AccountRegister()
    return HttpResponse(template.render(context, request))

@login_required
def accounts(request): 
    template = loader.get_template('accounts.html')
    users = User.objects.all()
    context = {
        'user_list': users 
    }
    return HttpResponse(template.render(context, request))

@login_required
def export(request, dropbox_id):  # downloads database in a csv 
    response = HttpResponse(content_type = 'text/csv')
    writer = csv.writer(response)
    writer.writerow(['Dropbox ID', 'Code 39', 'IMb', 'Date', 'Street Address', 'City', 'Zip Code', 'Status'])

    for data in EnvelopeScan.objects.all().filter(dropboxid=dropbox_id).values_list('dropboxid', 'imb', 'code39', 'date', 'streetaddress', 'city', 'zipcode', 'status'): 
        writer.writerow(data)

    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    return response 

@login_required
def create_dropbox(request): 
    template = loader.get_template('dropbox_list.html')

    if request.method == 'POST': 
        form = DropboxCreate(request.POST)
        if form.is_valid(): 
            id = form.cleaned_data["dropboxid"]
            form_data = {
                'dropboxid': form.cleaned_data["dropboxid"],
                'location_name': form.cleaned_data['location_name'],
                'coordinates': form.cleaned_data['coordinates']
            }

            serializer = DropboxSerializer(data=form_data)

            if serializer.is_valid(): 
                serializer.save()
                return redirect("list")



    context = {}
    return HttpResponse(template.render(context, request))

@login_required
def delete_dropbox(request, dropbox_id): 
    template = loader.get_template('dropbox_list.html')

    # delete 
    dropbox = get_object_or_404(Dropbox, dropboxid=dropbox_id)
    EnvelopeScan.objects.filter(dropboxid=dropbox_id).delete() # delete envelope scans with this dropbox id
    dropbox.delete()

    context = {}
    return redirect("list")

def account_logout(request): 
    logout(request)
    template = loader.get_template('home.html')
    context = {}
    return HttpResponse(template.render(context, request))

def handler404(request): 
    template = loader.get_template('404.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def handler403(request): 
    template = loader.get_template('403.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def handler500(request): 
    template = loader.get_template('500.html')
    context = {
    }
    return HttpResponse(template.render(context, request))



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def receive_sensor_data(request):
    serializer = EnvelopeSerializer(data=request.data)
    if serializer.is_valid(): # makes sure post request is valid 
        serializer.save() # inserts data 
        res = Response(serializer.data, status=status.HTTP_201_CREATED)  

        return res

    res = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return res

@api_view(['GET'])
@login_required
def obtain_auth_token(request, username): 
    if User.objects.filter(username=username).exists(): 
        user_requested = User.objects.get(username=username)
        token, _ = Token.objects.get_or_create(user=user_requested)
        return JsonResponse({"token": token.key})   
    else: 
        return JsonResponse({"msg": "User not found"})
