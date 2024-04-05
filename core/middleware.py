from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Profile  
class ProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        allowed_paths = [
            reverse('createProfile'),  
            reverse('login'),          
            reverse('logout'),         
        ]
        if request.path in allowed_paths:
            return self.get_response(request)

        try:
            profile = Profile.objects.get(user=request.user)
            if not self.has_required_fields(profile):
                raise ValueError("Required field is missing")
        except (Profile.DoesNotExist, ValueError):
            profile_url = reverse('createProfile')
            return HttpResponseRedirect(profile_url)

        return self.get_response(request)

    def has_required_fields(self, profile):
        if not profile.name or not profile.address or not profile.phone or not profile.email:
            return False
        return True