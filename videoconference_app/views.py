from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
import random
import string
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime  # Import datetime correctly
from .models import Recording,IsRecording
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'login.html', {'success': "Registration successful. Please login."})
        else:
            error_message = form.errors.as_text()
            return render(request, 'register.html', {'error': error_message})

    return render(request, 'register.html')


def login_view(request):
    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/dashboard")
        else:
            return render(request, 'login.html', {'error': "Invalid credentials. Please try again."})

    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html', {'name':""})


def videocall(request):
    return render(request, 'videocall.html', {'name': " "})

@login_required
def logout_view(request):
    logout(request)
    return redirect("/login")


def join_room(request):
    if request.method == 'POST':
        print("getting room id")
        roomID = request.POST['roomID']
        return redirect("/meeting?roomID=" + roomID)
    return render(request, 'joinroom.html')

@csrf_exempt
def save_recording(request):
    if request.method == 'POST':
        print("--post request received---")
        try:
            print("---got to data---")
            recorded_file = request.FILES.get('recordedData')  # Access file from request.FILES

            if recorded_file:
                # Generate a unique file name using the current date and time
                current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
                file_name = f"recording_{current_datetime}.mp4"

                # Create a new instance of Recording model
                new_recording = Recording(title=file_name)
                new_recording.file.save(file_name, recorded_file, save=True)

                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'No file received'})
        except Exception as e:
            print("---did not work--")
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Method not allowed'})

def view_recordings(request):
    recordings = Recording.objects.all()
    return render(request, 'admin.html', {'recordings': recordings})


def download_recording(request, recording_id):
    recording = get_object_or_404(Recording, pk=recording_id)
    file_path = recording.file.path  # Assuming 'file' is the FileField in your Recording model

    response = FileResponse(open(file_path, 'rb'), as_attachment=True)
    return response


class CheckRecording(APIView):
    def post(self, request):
        room_id = request.data.get("room_id")
        try:
            is_recording = IsRecording.objects.get(room_id=room_id)
            # If the object exists, return False
            return Response({
                "success": False,
                "message":"Recording already exists"}, 
                status=status.HTTP_200_OK)
        except IsRecording.DoesNotExist:
            # If the object does not exist, create a new object and return True
            IsRecording.objects.create(room_id=room_id)
            return Response({
                "success": True,
                "message":"Recording does not exist"}, 
                status=status.HTTP_201_CREATED)