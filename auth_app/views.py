import django
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

def home(request):
   return render(request, 'auth_app/home.html')

def signupuser(request):
   if request.method == 'GET':
      return render(request, 'auth_app/signupuser.html', {'form':UserCreationForm()})

   else:
      # Create a new user object
      if request.POST['password1'] ==request.POST['password2']:
         try:
            user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
            user.save()
            login(request, user)
            return redirect('dashboard')

         except IntegrityError:
            return render(request, 'auth_app/signupuser.html', {'form':UserCreationForm(), 'error':'This username has already been taken. Choose a unique one for you!'})

      else:
         return render(request, 'auth_app/signupuser.html',{'form': UserCreationForm(), 'error':'passwords did not match'}) 


def loginuser(request):
   if request.method == 'GET':
      return render(request, 'auth_app/loginuser.html',{'form':AuthenticationForm()})

   else: 
      #Login user object
      user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
      if user is None:
         return render(request, 'auth_app/loginuser.html',{'form':AuthenticationForm(), 'error':'username & password did not match'})

      else:
         login(request, user)
         return redirect('dashboard')


def logoutuser(request):
   if request.method == 'POST':
      logout(request)
      return redirect('home')

def dashboard(request):
   return render(request, 'auth_app/dashboard.html')

   
