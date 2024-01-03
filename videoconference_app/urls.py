from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register, name='register'),
    path('login/',views.login_view, name='login'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('meeting/',views.videocall, name='meeting'),
    path('logout/',views.logout_view, name='logout'),
    path('join/',views.join_room, name='join_room'),
    path("record-meeting",views.save_recording),
    path('view-recordings/', views.view_recordings, name='view_recordings'),
    path('download/<int:recording_id>/', views.download_recording, name='download_recording'),
    path('check-recording',views.CheckRecording.as_view()),
    path('',views.index, name='index'),

]