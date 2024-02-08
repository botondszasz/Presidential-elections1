from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import Profile

def home(request):
    return render(request, "index.html")

#Returns the page where users can apply for the elections
def user_candidate(request):
    if request.user.is_authenticated:
        current_user = request.user
        firstName = current_user.first_name
        lastName = current_user.last_name
        return render(request, "user-candidate.html", {'firstName': firstName, 'lastName': lastName })

#Returns the page where a user can see the candidates and also who has he/she voted for
def candidates(request):
    current_user = request.user
    firstName = current_user.first_name
    lastName = current_user.last_name
    if current_user.profile.hasVoted is False:
        return render(request, "candidates.html", {'firstName': firstName, 'lastName': lastName})
    
    search_id = current_user.profile.votedFor
    profile = Profile.objects.get(user_id=search_id)
    return render(request, "candidates.html", {'firstName': firstName, 'lastName': lastName, "profile":profile })

#Return the list of candidates
def list_candidates(request):
    all_candidates = Profile.objects.filter(hasApplied=True).exclude(user=request.user)
    current_user = request.user
    firstName = current_user.first_name
    lastName = current_user.last_name
    display = "block"
    if request.user.profile.hasVoted is True:
        search_id = current_user.profile.votedFor
        profile = Profile.objects.get(user_id=search_id)
        return render(request, "candidates.html", {"display":display, "profile":profile, "all_candidates":all_candidates, 'firstName': firstName, 'lastName': lastName})
    else:
        return render(request, "candidates.html", {"all_candidates":all_candidates, 'firstName': firstName, 'lastName': lastName})

#Hide the list of candidates
def hide_candidates(request):
    current_user = request.user
    firstName = current_user.first_name
    lastName = current_user.last_name
    display = "none"
    return render(request, "candidates.html", {"display":display, 'firstName': firstName, 'lastName': lastName})

#Lists the leaderboard
def show_leaderboard(request):
    all_candidates = Profile.objects.filter(hasApplied=True).order_by('-numberOfVotes')
    current_user = request.user
    firstName = current_user.first_name
    lastName = current_user.last_name
    return render(request, "main-page.html", {"all_candidates":all_candidates, 'firstName': firstName, 'lastName': lastName})

#Redirects to the main page, where the leaderboard is
def main_page(request):
    current_user = request.user
    firstName = current_user.first_name
    lastName = current_user.last_name
    return render(request, "main-page.html", {'firstName': firstName, 'lastName': lastName })

#Returns a user's profile page 
def profile(request):
     if request.user.is_authenticated:
          current_user = request.user
          firstName = current_user.first_name
          lastName = current_user.last_name
          return render(request, "profile.html", {'firstName': firstName, 'lastName': lastName})
     else:
          messages.success(request, "You must be logged in.")
          return redirect('home')        

#Return the page where users can set their social profiles
def social(request):
    current_user = request.user
    firstName = current_user.first_name
    lastName = current_user.last_name
    return render(request, "social.html", {'firstName': firstName, 'lastName': lastName })

#Redirects to the page where the winner is displayed
def winner(request):
    current_user = request.user
    firstName = current_user.first_name
    lastName = current_user.last_name
    winner = Profile.objects.filter(hasApplied=True).order_by('-numberOfVotes').first()
    return render(request, "winner.html",{"winner":winner, 'firstName': firstName, 'lastName': lastName })
