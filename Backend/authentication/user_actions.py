from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import Profile

#Verifies if a user has applied, if not, he can apply
def apply(request, user_id):
    if request.user.is_authenticated:
        current_user = User.objects.get(pk=user_id)
        firstName = current_user.first_name
        lastName = current_user.last_name
        if request.user.profile.hasApplied is False:
            current_user.profile.hasApplied = True
            current_user.save()
            messages.success(request, "Congratulations! Your application was successful!")
            return render(request, "profile.html", {'firstName': firstName, 'lastName': lastName})
        else:
            messages.success(request, "You have already applied.")
            return render(request, "profile.html", {'firstName': firstName, 'lastName': lastName})
    else:
        messages.success(request, "You must be logged in.")
        return render(request, "profile.html", {'firstName': firstName, 'lastName': lastName})
    
#Verifies if a user has applied, in case which he/she can vote
#Also verifies if he/she has already voted or not
#Registers the vote and increases the number of votes for the chosen person
def vote(request, pk):
    if request.user.is_authenticated:
        current_user = request.user
        firstName = current_user.first_name
        lastName = current_user.last_name
        if request.user.profile.hasApplied is False:
            messages.success(request, "You must be a candidate to vote others.")
            return render(request, "profile.html", {'firstName': firstName, 'lastName': lastName })
        else:
            if request.user.profile.hasVoted is True:
                messages.success(request, "Sorry. You can vote only once.")
                return render(request, "profile.html", {'firstName': firstName, 'lastName': lastName })
            else:
                profile = Profile.objects.get(user_id=pk)
                profile.numberOfVotes += 1
                profile.save()
                current_user.profile.votedFor = profile.user.id
                current_user.profile.hasVoted = True
                current_user.save()
                messages.success(request, "You successfully voted.")
                return render(request, "profile.html", {'firstName': firstName, 'lastName': lastName })
    else:
        messages.success(request, "You must be logged in.")
        return redirect('home')
    
#Redirects to another user's profile page
#A user can be redirected to his own profile page
#If a user is not a candidate, he/she can't see other people's profile page
def view_profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        current_user = request.user
        firstName = current_user.first_name
        lastName = current_user.last_name

        if request.user.id == profile.user.id:
            return render(request, "profile.html", {'firstName': firstName, 'lastName': lastName })

        if request.user.profile.hasApplied is True:
            return render(request, "other-profile.html", {"profile":profile})
        else:
            current_user = request.user
            firstName = current_user.first_name
            lastName = current_user.last_name
            messages.success(request, "You must be a candidate to see other profile.")
            return render(request, "profile.html", {'firstName': firstName, 'lastName': lastName })
    else:
        messages.success(request, "You must be logged in.")
        return redirect('home')
    
#A user can remove his vote
def remove_vote(request):
    if request.user.is_authenticated:
        current_user = request.user
        firstName = current_user.first_name
        lastName = current_user.last_name
        search_id = current_user.profile.votedFor
        profile = Profile.objects.get(user_id=search_id)
        current_user.profile.hasVoted = False
        current_user.profile.votedFor = None
        profile.numberOfVotes -= 1
        current_user.save()
        profile.save()
        messages.success(request, "You removed your vote.")
        return render(request, "profile.html", {'firstName': firstName, 'lastName': lastName })
    else:
        messages.success(request, "You must be logged in.")
        return redirect('home')
    
#A user can remove his application
#This also means that his vote is removed (if he/she voted for somebody)
#and the person he/she voted for, loses a vote 
def remove_application(request):
    if request.user.is_authenticated:
        current_user = request.user
        firstName = current_user.first_name
        lastName = current_user.last_name
        
        if current_user.profile.numberOfVotes > 0:
            current_user.profile.numberOfVotes = 0
            myVoters = Profile.objects.filter(votedFor=current_user.id).update(hasVoted=False)
                
            #remove hasVoted from those who voted for them                
        
        if current_user.profile.hasVoted is True:
            search_id = current_user.profile.votedFor
            profile = Profile.objects.get(user_id=search_id)
            profile.numberOfVotes -= 1
            current_user.profile.hasVoted = False
            current_user.profile.votedFor = None
            profile.save()

        if current_user.profile.hasApplied is True:
            current_user.profile.hasApplied = False

        current_user.save()
        messages.success(request, "You removed your application.")
        return render(request, "profile.html", {'firstName': firstName, 'lastName': lastName })
    else:
        messages.success(request, "You must be logged in.")
        return redirect('home')
    
    #Saves the changes made by a user regarding social profiles
def submit_socials(request):
    if request.user.is_authenticated:
        current_user = request.user
        firstName = current_user.first_name
        lastName = current_user.last_name

        if request.method == "POST":
            facebook = request.POST['facebook']
            instagram = request.POST['instagram']
            linkedin  = request.POST['linkedin']

            current_user.profile.linkFacebook = facebook
            current_user.profile.linkInstagram = instagram
            current_user.profile.linkLinkedin = linkedin
            current_user.save()

            messages.success(request, "Successfully updated social media links.")
            return render(request, "profile.html", {'firstName': firstName, 'lastName': lastName })
    else:
        messages.success(request, "You must be logged in.")
        return redirect('home')

