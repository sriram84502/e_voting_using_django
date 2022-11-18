import imp
from django.http import HttpResponseRedirect,HttpResponse
from django.core.mail import BadHeaderError, send_mail
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render,redirect
from .helper import MessageHandler,MessageHandler1
from .models import participants,CustomUser,Profile,Voters,Votingrelease,Resultrelease
from django.contrib import messages
import random
from django.contrib.auth import authenticate,login,logout
from .forms import CustomUserCreationForm
# Create your views here.

@login_required(login_url="/signin/")
def participant(request):
    parts=participants.objects.all()
    return render(request,'authenticate/participants.html',{'parts':parts})
    
    
@login_required(login_url="/signin/")
def vote(request):
    voter_obj=Voters.objects.filter(user=request.user)
    check_vote=Votingrelease.objects.get(id=1)
    parts=participants.objects.all()
    if check_vote.voting==0:
        return render(request,'authenticate/comingsoon.html',{'vote':check_vote})
    if not(voter_obj):
        return render(request,'authenticate/vote.html',{'parts':parts})
    else:
        return render(request,'authenticate/error.html')

@login_required(login_url="/signin/")
def results(request):
    parts=participants.objects.all()
    check_vote=Resultrelease.objects.get(id=1)
    print(check_vote)
    if check_vote.result==1:
        return render(request,'authenticate/results.html',{'parts':parts})
    else:
        return render(request,'authenticate/comingsoon.html',{'vote':check_vote})

def signin(request):
    if request.method == 'POST':
        username=request.POST['aadhar']
        password=request.POST['Password']
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                otp1=random.randint(100000,999999)
                profile = Profile.objects.get(aadhar1 = username)
                profile.otp=otp1
                profile.save()
                messagehandler=MessageHandler(profile.phone1,profile.otp).send_otp_via_message()
                return redirect(f'/otp/{profile.uid}')
                
            else:
                messages.info(request,'account is not active')
                return redirect('signin')
        else:
            messages.info(request,'Invalid credentials')
            return redirect('signin')
    else:
        return render(request,'authenticate/signin.html')

def signup(request):
    context = {}
    if request.method == "POST":
        userform = CustomUserCreationForm(data=request.POST)
        phonenum = request.POST.get('phone')
        if userform.is_valid():
            user = userform.save()
            user.save()
            profile=Profile.objects.create(user=user,phone1=user.phone,aadhar1=user.username)
            profile.save()
            return redirect('signin')
        else:
            print(userform.errors)
            messages.info(request,userform.errors)
            return redirect('signup')
    else:
        userform=CustomUserCreationForm()
    return render(request,'authenticate/signup.html',{'userform':userform})    


def home(request):
    parts=participants.objects.all().count()
    users=CustomUser.objects.all().count()
    voters=Voters.objects.all().count()
    remaining=users-voters
    return render(request,'authenticate/home.html',{'userform':CustomUser,'remain':remaining,'users':users,'parts':parts,'voters':voters})

@login_required(login_url="/signin/")
def about(request):
    return render(request,'authenticate/about.html')

def otpVerify(request,uid):
    if request.method=="POST":
        otp = request.POST.get('otp')
        profile = Profile.objects.get(uid = uid)
        if otp == profile.otp:
            login(request,profile.user)
            return redirect('about')
        messages.info(request,"OTP is invalid")
        return redirect('/otp/{uid}')
    return render(request,'authenticate/otp.html')

@login_required(login_url="/signin/")
def logout_acc(request):
    logout(request)
    return HttpResponseRedirect(reverse(home))

@login_required(login_url="/signin/")   
def voters(request,participants_id):
    voter_obj=Voters.objects.filter(user=request.user)
    if not(voter_obj):
        print(participants_id,participants.id)
        part_obj=participants.objects.filter(id=participants_id).first()
        part_obj.votes=part_obj.votes+1
        part_obj.save()
        voter=Voters.objects.create(user=request.user)
        voter.save()
        profile = Profile.objects.get(aadhar1 = request.user)
        messagehandler=MessageHandler1(profile.phone1).send_otp_via_message()
        return render(request,'authenticate/sucess.html')
    else:
        return render(request,'authenticate/error.html')


def aboutus(request):
    return render(request,'authenticate/aboutus.html')


def send_email(request):
    subject = request.user 
    name = request.user.name
    gap = " "
    message = request.POST.get('message')
    from_email = request.POST.get('email')
    if message and from_email:
        try:
            send_mail(str(subject) + str(gap) + str(name), message, from_email, ['184502@sasi.edu.in'],fail_silently=False)
        except BadHeaderError:
            messages.info(request,'Invalid header found')
            return redirect('aboutus')
        messages.info(request,'Mail is sucessfully sent')
        return redirect('aboutus')
    else:
        messages.info(request,'Make sure all fields are entered and valid.')
        return redirect('aboutus')