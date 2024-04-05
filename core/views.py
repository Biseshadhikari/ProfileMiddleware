from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .models import *
from .forms import ProfileForm
# Create your views here.

def home(request): 
    if request.user.is_authenticated:
        return render(request,'index.html')
    else: 
        return redirect('login')


# accounts/views.py

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('home')  # Adjust 'home' to your desired route
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, "login.html")








def createProfile(request):
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user  = request.user).first()
        if request.method == 'POST':
            if not profile:
            
                form = ProfileForm(request.POST)
                if form.is_valid():
                    forms = form.save(commit = False)
                    forms.user = request.user
                    forms.save()
                    return redirect('/')  # Redirect as needed
            else: 
                form = ProfileForm(request.POST,instance=profile)
                if form.is_valid():
                    forms = form.save(commit = False)
                    forms.user = request.user
                    forms.save()
                    return redirect('/')  # Redirect as needed

        else:
            if profile:
                form = ProfileForm(instance=profile)
            else:
                form = ProfileForm()
        return render(request, 'profile.html', {'form': form})
    else:
        return redirect('login')


def logout_view(request):
    logout(request)
    return redirect('/')