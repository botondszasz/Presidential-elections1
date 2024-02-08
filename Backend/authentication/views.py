from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import Profile

def home(request):
    return render(request, "index.html")

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        firstName = request.POST['firstName']
        lastName  = request.POST['lastName']
        email = request.POST['email']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist")
            return redirect('register')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered")
            return redirect('login')
        
        if len(username)>30:
            messages.error(request, "Username must be shorter than 30 characters")
            return redirect('register')
        
        if password != confirmPassword:
            messages.error(request, "Please make sure your passwords match")
            return redirect('register')

        if not username.isalnum():
            messages.error(request, "Username must contain only letter and numbers")
            return redirect('register')
        
        user = User.objects.create_user(
            username,
            first_name=firstName,
            last_name=lastName,
            email=email,
            password=password,
        )
    
        user.save()

        messages.success(request, "Your account has been successfully created.")

        return redirect('login') 

    return render(request, "register.html")
    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not User.objects.filter(username=username):
            messages.error(request, "Username does not exist")
            return redirect('login')

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            firstName = user.first_name
            return render(request, "main-page.html", {'firstName': firstName})
        else: 
            messages.error(request, "Incorrect email/password combination")
            return redirect('login')
    return render(request, "login.html")

def logout(request):
    auth_logout(request)
    messages.success(request, "Logged out.")
    return redirect('home')
    
#Returns the page where users can change their personal information
def update_description(request):
    if request.user.is_authenticated:
          current_user = request.user
          firstName = current_user.first_name
          lastName = current_user.last_name
          return render(request, "update-description.html", {'firstName': firstName, 'lastName': lastName})
    else:
          messages.success(request, ("You must be logged in."))
          return redirect('home')    

#Update user personal info
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

#Returns the page where users can apply for the elections
def user_candidate(request):
    if request.user.is_authenticated:
        current_user = request.user
        firstName = current_user.first_name
        lastName = current_user.last_name
        return render(request, "user-candidate.html", {'firstName': firstName, 'lastName': lastName })

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

#Return the page where users can set their social profiles
def social(request):
    current_user = request.user
    firstName = current_user.first_name
    lastName = current_user.last_name
    return render(request, "social.html", {'firstName': firstName, 'lastName': lastName })

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

#Redirects to the page where the winner is displayed
def winner(request):
    current_user = request.user
    firstName = current_user.first_name
    lastName = current_user.last_name
    winner = Profile.objects.filter(hasApplied=True).order_by('-numberOfVotes').first()
    return render(request, "winner.html",{"winner":winner, 'firstName': firstName, 'lastName': lastName })
