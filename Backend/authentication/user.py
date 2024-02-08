from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

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
    
def logout(request):
    auth_logout(request)
    messages.success(request, "Logged out.")
    return redirect('home')