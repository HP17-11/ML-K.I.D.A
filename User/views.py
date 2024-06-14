import datetime
import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, FiledataForm
from .models import *
from object_detection import count_objects_in_video
from django.contrib import messages


def loginUser(request):
    page = 'login'
    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username'].lower()
        password = request.POST['password']
        # print(username, password)
        try:
            user = User.objects.get(username=username)
            print(user)
        except User.DoesNotExist:
            print('User not found')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            LoginHistory.objects.create(user=user, login_time=datetime.datetime.now())
            return redirect('homepage')
        else:
            print(request, 'Invalid username or password.')
            messages.error(request, 'Invalid username or password!!!')
    return render(request, 'User/login_register.html', {'page': page})


def logoutUser(request):
    logout(request)
    print(request, 'User was logged out!')
    return redirect('loginUser')


def createUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "User is created successfully!")

            return redirect('loginUser')

        else:
            print(request, 'An error has occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'User/login_register.html', context)


@login_required(login_url='loginUser')
def homepage(request):

    form = FiledataForm()
    try:
        owner = Profile.objects.get(username=request.user.username)
        print(owner.profile_id)
    except:
        owner =''

    if request.method == 'POST':

        print('started processing')
        form = FiledataForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = form.cleaned_data['video_file']

            with open('temp_video.mp4', 'wb') as temp_file:
                for chunk in video_file.chunks():
                    temp_file.write(chunk)
            result = count_objects_in_video('temp_video.mp4', "videos/output.mp4")
            os.remove('temp_video.mp4')

            file = form.save(commit=False)
            file.owner = owner

            file.predatory_mites = result["predatory-mites"]
            file.feeder_mites = result["feeder-mites"]
            file.save()

            print(result)
            print(file.predatory_mites)
            print(file)
            messages.success(request, "File is sucessfully uploaded and Processed!")
            print(owner)
            context = {'file':file, 'owner':owner}
            return render(request, 'hompage.html', context)
    print('hello outside')
    print(owner)

    context = {'form': form, 'owner': owner}
    return render(request, 'hompage.html', context)

@login_required(login_url='loginUser')
def admin_panel(request):
    if request.user.is_superuser:
        users = Profile.objects.all()
        return render(request, 'User/admin_panel.html', {'users': users})
    else:
        messages.error(request, 'You do not have permission to access the admin page!!!')
        return redirect('homepage')


def user_profile(request):
    user_p = Profile.objects.get(username=request.user.username)
    videos = filedata.objects.filter(owner=user_p)
    return render(request, 'User/user_profile.html', {'profile': user_p, 'videos': videos})


def owners_profile(request, pk):
    user_p = Profile.objects.get(profile_id=pk)
    videos = filedata.objects.filter(owner=user_p)
    login_history = LoginHistory.objects.filter(user=user_p)
    print(login_history)
    return render(request, 'User/user_profile.html', {'profile': user_p, 'videos': videos, 'login_history':login_history})
