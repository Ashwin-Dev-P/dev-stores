from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import *

import os, sys
sys.path.insert(1, os.getcwd()) 
from ThumkiStores.models import *

def sign_up(request):
    if(request.method == 'GET'):
        mydata = General_info.objects.first()
        categories = Category.objects.all()
        return render(request,'account/signup.html',{'title':'sign up','mydata':mydata,'categories':categories })
    elif(request.method == 'POST'):
        username = request.POST['username']
        if(User.objects.filter(username=username).exists()):
            messages.error(request,'Username is taken')
            return redirect('sign_up')
        elif(len(username) < 1 ):
            messages.error(request,'Enter an username.')
            return redirect('sign_up') 
            

        email = request.POST['email']
        if(User.objects.filter(email=email).exists()):
            messages.error(request,"E-mail is already in use.")
            return redirect('sign_up')
        elif(len(email) < 5):
            messages.error(request,"Enter a valid email id.")
            return redirect('sign_up')
        
        
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if(len(password1) < 1 or len(password2) < 1  ):
            messages.error(request,"Enter the password")
            return redirect('sign_up')
        elif(password1 != password2):
            messages.error(request,"Both the passwords do not match.")
            return redirect('sign_up')
        
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        if(len(first_name) < 1):
            first_name = ''
        if(len(last_name) < 1):
            last_name = ''

        user = User.objects.create_user(username=username,email=email,password=password1,first_name=first_name,last_name=last_name)
        try:
            user.save()
        except:
            messages.error(request,"Invalid form data")
            return redirect('sign_up')
        messages.success(request,"Account created successfully.")
        auth.login(request,user)
        
        if( 'subscribe' in request.POST ):
            if( request.POST['subscribe'] ):
                subscription_form = Subscription(email=email)
                try:
                    subscription_form.save()
                except:
                    return redirect('sign_up')       
        return redirect('sign_up')
    else:
        messages.error(request,'This method cannot be handled.')
        return render(request,'error.html',{'title':'Error','mydata':mydata})
        
        
def login(request):
    if(request.method == 'GET'):
        mydata = General_info.objects.first()
        categories = Category.objects.all()
        return render(request,'account/login.html',{'title':'login','mydata':mydata,'categories':categories})
    elif(request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            messages.success(request,'Logged in successfully.')
            auth.login(request,user)
            return redirect('')
        else:
            messages.error(request,'Invalid credentials.')
            return redirect('login')
        
    else:
        messages.error(request,'This method cannot be handled.')
        return render(request,'error.html',{'title':'Error','mydata':mydata})       
