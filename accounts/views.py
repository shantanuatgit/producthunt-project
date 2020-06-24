from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
def signup(request):
    if request.method=="POST":
        # user has info and want account now.
        if request.POST['password1']==request.POST['password2']:
            # check if user name already exist.
            try:
                user=User.objects.get(username=request.POST['Username'])
                return render(request,'accounts/signup.html',{'error':'Username already taken'})
            except User.DoesNotExist:
                user=User.objects.create_user(request.POST['Username'], password=request.POST['password1'])
                auth.login(request,user) #this line log that user in.
                return redirect('home')
        else:
            return render(request,'accounts/signup.html',{'error':'please confirm password again'})
    else:
        # user wants to enter info.
        return render(request,'accounts/signup.html')



def login(request):
    if request.method=="POST":
        user = auth.authenticate(username=request.POST['Username'],password=request.POST['password'])
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return render(request,'accounts/login.html',{'error':'username or password is incorrect.'})
    else:
        return render(request,'accounts/login.html')



def logout(request):
    if request.method=="POST":
        auth.logout(request)
        return redirect('home')
