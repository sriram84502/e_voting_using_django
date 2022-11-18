from django.urls import path
from . import views
"""from django.contrib.auth import as auth_views"""
urlpatterns = [
    path('',views.home,name='home'),
    path('participants/',views.participant,name='participants'),
    path('otp/<uid>', views.otpVerify, name='otp'),
    path('vote/',views.vote,name='vote'),
    path('results/',views.results,name='results'),
    path('voters/<int:participants_id>',views.voters,name='voters'),
    path('signin/',views.signin,name='signin'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout_acc,name='logout'),
    path('about/',views.about,name='about'),
    path('aboutus/',views.aboutus,name='aboutus'),
    path('send_email',views.send_email,name='send_email'),
]

