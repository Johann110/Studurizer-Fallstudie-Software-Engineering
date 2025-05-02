import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _

from accounts.models import UserProfile, CustomUser
from accounts.forms import UserProfileForm

def profile_detail(request, id):
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

def profile_edit(request):
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

def profile_delete_picture(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.profile_picture:
            if os.path.isfile(profile.profile_picture.path):
                try:
                    os.remove(profile.profile_picture.path)
                except OSError as e:
                    messages.error(request, 'Das Profilbild konnte nicht gelöscht werden: ' + str(e))
            profile.profile_picture = None
            profile.save()

            messages.success(request, _('Profilbild wurde erfolgreich gelöscht.'))
        else:
            messages.info(request, _('Kein Profilbild zum Löschen vorhanden.'))

    except UserProfile.DoesNotExist:
        messages.error(request, _('Profil konnte nicht gefunden werden.'))

    return redirect('profile_edit')


def profile_delete_signature(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.signature:
            if os.path.isfile(profile.signature.path):
                try:
                    os.remove(profile.signature.path)
                except OSError as e:
                    messages.error(request, 'Die Unterschrift konnte nicht gelöscht werden: ' + str(e))
            profile.signature = None
            profile.save()

            messages.success(request, _('Unterschrift wurde erfolgreich gelöscht.'))
        else:
            messages.info(request, _('Keine Unterschrift zum Löschen vorhanden.'))

    except UserProfile.DoesNotExist:
        messages.error(request, _('Profil konnte nicht gefunden werden.'))

    return redirect('profile_edit')

