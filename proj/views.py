from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import sys
sys.path.insert(0, '/home/luiz/proj/portfolio')



def home(request):
    print(request.user.is_authenticated)
    if not request.user.is_authenticated:
        redirect('login')  
	# Checking to see if theyy ar logging in
    if request.method == 'POST':
        usernam        # Authenticatee = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.error(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')
    else:
        if request.user.is_authenticated:
            stocks = request.user.stocks_followed.all().prefetch_related('alert_rules')
            return render(request, 'home.html', {'stocks': stocks,})
        else:
            return render(request, 'home.html', {})
        
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.error(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')
    else:
        return render(request, 'home.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')



