from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from loginsystem.settings import EMAIL_HOST_USER
# Create your views here.

def send(email):
    subject = 'You have been succesfully signed up'
    message = 'Hello world'
    from_email = 'doreamonshinchan58@gmail.com'
    recipient_list = [email]

    # Sending the email
    send_mail(subject, message, from_email, recipient_list)
    
def HomePage(request):
    return render(request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if User.objects.filter(username=uname).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return render(request, 'signup.html')
        try:
            # Create the user if validation passes
            my_user = User.objects.create_user(username=uname, email=email, password=pass1)
            my_user.save()
            messages.success(request, 'User has been created successfully')
            send(email)
            return redirect('home')  # Or redirect to a different page
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
            return render(request, 'signup.html')
    
    return render(request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        print(user)
        if user is not None:
            login(request,user)

            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')
