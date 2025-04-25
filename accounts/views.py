from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _

from accounts.models import UserProfile, CustomUser
from accounts.profile_forms import UserProfileForm


@login_required
def profile_detail(request, id):
    """
    View function to display user profile
    """
    logged_in_user = get_object_or_404(CustomUser, id=id)

    try:
        profile = UserProfile.objects.get(user=logged_in_user)
    except UserProfile.DoesNotExist:
        profile = None

    context = {
        'logged_in_user': logged_in_user,
        'profile': profile
    }

    return render(request, "accounts/profile_detail.html", context)


@login_required
def profile_edit(request):
    """
    View function to edit user profile
    """
    # Get the user's profile or create it if it doesn't exist
    user = request.user
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={'description': '', 'profile_picture': None}
    )

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your profile has been updated successfully.'))
            return redirect('profile', id=user.id)
    else:
        form = UserProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
    }

    return render(request, 'accounts/profile_edit.html', context)