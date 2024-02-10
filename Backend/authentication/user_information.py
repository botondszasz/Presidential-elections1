from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout as auth_logout

# Update user personal info
def update_profile(request, user_id):
    current_user = User.objects.get(pk=user_id)
    description = request.GET.get('description')
    first = request.GET.get('first')
    last = request.GET.get('last')
    current_user.profile.user_bio = description
    current_user.first_name = first
    current_user.last_name = last
    firstName = current_user.first_name
    lastName = current_user.last_name
    current_user.save()
    messages.success(request, "Your update was successfull.")
    return render(request, "profile.html", {'firstName': firstName, 'lastName': lastName })