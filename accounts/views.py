from django.contrib.auth import user_logged_in
from django.contrib.auth.models import User
from django.shortcuts import render

from accounts.models import UserProfile, CustomUser


# Create your views here.

def profile_detail(request, id):
    user_logged_in = None
    try:
        user_logged_in = CustomUser.objects.get(id=id)
        profile = UserProfile.objects.get(user=user_logged_in)
    except UserProfile.DoesNotExist:
        profile = None

    context = {
        profile : profile,
        user_logged_in : user_logged_in
    }
    return render(request, "accounts/profile_detail.html", context)
