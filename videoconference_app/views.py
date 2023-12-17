from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
import random
import string
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime  # Import datetime correctly
from .models import Recording
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
    return render(request, 'dashboard.html', {'name': request.user.first_name})


def videocall(request):
    return render(request, 'videocall.html', {'name': request.user.first_name + " " + request.user.last_name})

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

@api_view(['POST'])
def create_room(request):
    if request.method == 'POST':
        # Get the name from the request body
        name = request.data.get('name')

        # Generate a random 4-digit room ID
        room_id = ''.join(random.choices(string.digits, k=4))

        # Construct the redirect URL with the room ID
        redirect_url = f'/meeting/?roomId={room_id}'

        # Return room ID and redirect URL in the response
        return Response({'room_id': room_id, 'redirect_url': redirect_url})

    return Response({'error': 'Invalid request'})