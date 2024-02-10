from datetime import date
import math
from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Profile
from .models import Event

def home(request):
    return render(request, "index.html")

# Returns the page where users can apply for the elections
def user_candidate(request):
    if request.user.is_authenticated:
        current_user = request.user
        firstName = current_user.first_name
        lastName = current_user.last_name
        return render(request, "user-candidate.html", {'firstName': firstName, 'lastName': lastName })

# Returns the page where a user can see the candidates and also who has he/she voted for
def candidates(request):
    current_user = request.user
    firstName = current_user.first_name
    lastName = current_user.last_name
    if current_user.profile.hasVoted is False:
        return render(request, "candidates.html", {'firstName': firstName, 'lastName': lastName})
    
    search_id = current_user.profile.votedFor
    profile = Profile.objects.get(user_id=search_id)
    return render(request, "candidates.html", {'firstName': firstName, 'lastName': lastName, "profile":profile })

# Return the list of candidates
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

# Hide the list of candidates
def hide_candidates(request):
    current_user = request.user
    firstName = current_user.first_name
    lastName = current_user.last_name
    display = "none"
    return render(request, "candidates.html", {"display":display, 'firstName': firstName, 'lastName': lastName})

# Lists the leaderboard
def show_leaderboard(request):
    all_candidates = Profile.objects.filter(hasApplied=True).order_by('-numberOfVotes')
    current_user = request.user
    firstName = current_user.first_name
    lastName = current_user.last_name
    return render(request, "main-page.html", {"all_candidates":all_candidates, 'firstName': firstName, 'lastName': lastName})

# Redirects to the main page, where the leaderboard is
def main_page(request):
    current_user = request.user
    firstName = current_user.first_name
    lastName = current_user.last_name
    return render(request, "main-page.html", {'firstName': firstName, 'lastName': lastName })

# Returns a user's profile page 
def profile(request):
    if request.user.is_authenticated:
        current_user = request.user
        firstName = current_user.first_name
        lastName = current_user.last_name
        now  = timezone.now()
        
        first_event = Event.objects.filter(event_start_date__date__gte=now).order_by('event_start_date')[:1].get()
        
        # if(not first_event or first_event.event_start_date > now):
        #     last_event_finished = Event.objects.filter(event_end_date__date__lte=now).order_by('-event_end_date').first()
        #     if(last_event_finished):
        #         first_place = Profile.objects.filter(hasApplied=True).order_by('-numberOfVotes').first()
        #         last_event_finished.winner = first_place.user.get_full_name.title
        #         condidates = Profile.objects.filter(hasApplied=True).update(numberOfVotes=0)
        
        if(not first_event):
            message = 'There are no voting rounds scheduled.'
            style = 'h4'
            vote_display = 'none'
            return render(request, "profile.html", {'firstName': firstName, 'lastName': lastName, 'message':message, 'style':style, 'vote_display':vote_display})
        else:
            if(first_event.event_start_date>now):
                message = 'There are no voting rounds in progress.'
                style = 'h4'
                vote_display = 'none'
                return render(request, "profile.html", {'firstName': firstName, 'lastName': lastName, 'message':message, 'style':style, 'vote_display':vote_display})
            else:
                timeDiff = first_event.event_end_date - now
                timeDiffMS = timeDiff.total_seconds() * 1000
                seconds = math.floor((timeDiffMS % (1000 * 60)) / 1000) 
                minutes = math.floor((timeDiffMS % (1000 * 60 * 60)) / (1000 * 60)) 
                hours  = math.floor((timeDiffMS % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)) 
                days = math.floor(timeDiffMS / (1000 * 60 * 60 * 24))  
                data = {
                    'days' : days,
                    'hours' : hours,
                    'minutes' : minutes,
                    'seconds' : seconds,
                }
                return render(request, "profile.html", {'firstName': firstName, 'lastName': lastName, 'data':data})
    else:
        messages.success(request, "You must be logged in.")
        return redirect('home')        

# Return the page where users can set their social profiles
def social(request):
    current_user = request.user
    firstName = current_user.first_name
    lastName = current_user.last_name
    return render(request, "social.html", {'firstName': firstName, 'lastName': lastName })

# Redirects to the page where the winner is displayed
def winner(request):
    current_user = request.user
    firstName = current_user.first_name
    lastName = current_user.last_name
    rounds = Event.objects.order_by('-event_start_date')
    return render(request, "winner.html",{"rounds":rounds, 'firstName': firstName, 'lastName': lastName })

# Returns the page where users can change their personal information
def update_description(request):
    if request.user.is_authenticated:
          current_user = request.user
          firstName = current_user.first_name
          lastName = current_user.last_name
          return render(request, "update-description.html", {'firstName': firstName, 'lastName': lastName})
    else:
          messages.success(request, ("You must be logged in."))
          return redirect('home')    
