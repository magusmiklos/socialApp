from django.contrib.auth.decorators import login_required
from django.core.serializers.base import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from accounts.forms import PostForm, ProfileForm
from accounts.models import Post, Profile, Follow
from django.http import JsonResponse
from collections import UserDict
from django.contrib.auth.models import User

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('explore')  # Replace 'home' with your desired redirect URL
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/login.html')

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Profile.objects.create(user=request.user)
            return redirect('explore')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

def user_profile(request):
    user_posts = Post.objects.filter(user=request.user).order_by('-created_at')

    profile = Profile.objects.get(user=request.user)

    return render(request, 'accounts/profile.html', {'user':request.user, 'user_posts':user_posts, 'profile':profile})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def create_post(request):
    if request.method == 'POST':
       form = PostForm(request.POST)
       form.request = request
       if form.is_valid():
           form.save()
           return redirect('profile')
    else:
        form = PostForm()
    return render(request, 'accounts/create.html', {'form': form})

@login_required
def load_post(request, id):
    post = get_object_or_404(Post,id=id)
    return render(request, 'accounts/post.html', {'post': post})

@login_required
def delete_post(request, id):
    post = get_object_or_404(Post,id=id)

    if post.user == request.user:
        post.delete()

    return redirect('profile')

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('edit_profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {'form': form, 'profile':profile})

@login_required
def toggle_follow(request,id):
    user = request.user
    target_user = get_object_or_404(User,id=id)

    if request.method == 'POST':

        follow = Follow.objects.filter(follower=user,following=target_user).first()

        if follow != None:
            follow.delete()
            return JsonResponse({'success':True, 'is_followed':False})
        Follow.objects.create(follower=user,following=target_user)
        return JsonResponse({'success':True, 'is_followed':True})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})
