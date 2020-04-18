from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.mail import send_mail
from app.models import student
from app.models import Hostel
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,permission_required

def forgot(request):
    if (request.method == 'GET'):
        return render(request,'accounts/forgot.html')
    elif (request.method == 'POST'):
        if not request.POST["roll"]:
            return render(request,'accounts/forgot.html',{'error':{
                'text':'Registeration Number field cannot be left empty!'
            }})       
        else:
            # send_mail('Forgot Password', request.POST["roll"],request.POST["email"], 'nishu1952000@gmail.com')
            return render(request,'accounts/forgot.html')
@login_required
def change(request):
    if (request.method == 'GET'):
        #just want to view the change password page
        return render(request,'accounts/signup.html')
    elif (request.method == 'POST'):
        #data was filled and user is awaiting
        if not request.POST["password1"]:
            return render(request,'accounts/change.html',{'error':{
                'text':'passwords field cannot be left empty!'
            }})
        if (request.POST["password1"] == request.POST["password2"]):
            try:
                user = User.objects.get(username = request.POST["username"])
                return render(request,'accounts/signup.html',{'error':{
                    'text':'User already exists!'
                }})
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST["username"],password=request.POST["password1"])
                auth.login(request,user)
                objct=student()
                objct.user=request.user
                objct.save()

            return render(request,'accounts/details.html')
        else:
            return render(request,'accounts/signup.html',{'error':{
                'text':'Passwords don\'t match!'
            }})
def signup(request):
    if (request.method == 'GET'):
        #just want to view the sign up page
        return render(request,'accounts/signup.html')
    elif (request.method == 'POST'):
        #sign up data was filled and user is awaiting account creation
        if not request.POST["username"]:
            return render(request,'accounts/signup.html',{'error':{
                'text':'Username field cannot be left empty!'
            }})
        if (request.POST["password1"] == request.POST["password2"]):
            try:
                user = User.objects.get(username = request.POST["username"])
                return render(request,'accounts/signup.html',{'error':{
                    'text':'User already exists!'
                }})
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST["username"],password=request.POST["password1"])
                auth.login(request,user)
                objct=student()
                objct.user=request.user
                objct.save()

            return render(request,'accounts/details.html')
        else:
            return render(request,'accounts/signup.html',{'error':{
                'text':'Passwords don\'t match!'
            }})

def login(request):
    if request.method=='POST':
        user=auth.authenticate(username=request.POST["username"],password=request.POST["password"])
        if user is not None:
            auth.login(request,user)
            
            return redirect('master_home')
        else:
            return render(request,'mainpage/master.html',{'error':{
                'text':'Username or password is not correct'
            }})
    else:
        return render(request,'accounts/login.html')

def logout(request):
    if request.method=='POST':
        auth.logout(request)
        return redirect('master_home')
# def details(request):def update_balance(username,balance):


@login_required
def details(request):
    if request.method == 'POST':
        if request.POST["nam"] and request.POST["email"] and request.POST["phone"]:
            usersn=request.user
            obj=student.objects.get(user=usersn)
            # obj.user = request.user
            obj.name = request.POST["nam"]
            obj.email=request.POST["email"]
            obj.phone=request.POST["phone"]
            obj.Hostel=Hostel.objects.get(id=request.POST["Hostel"])
            obj.save()
            return redirect('master_home')
        else:
                return render(request,'accounts/details.html',{'error':
                {
                'text':'Please fill all required information'
                }})
    else:
        return render(request,'accounts/details.html')