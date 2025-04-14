from django.contrib.auth import user_logged_in
from django.contrib.auth.models import User
from django.shortcuts import render

from accounts.models import UserProfile, CustomUser


# Create your views here.

def profile_detail(request, id):
    logged_in_user = None
    try:
        logged_in_user = CustomUser.objects.get(id=id)
        profile = UserProfile.objects.get(user=logged_in_user)
    except UserProfile.DoesNotExist:
        profile = None

    context = {
        profile : profile,
        logged_in_user : logged_in_user
    }
    return render(request, "accounts/profile_detail.html", context)
