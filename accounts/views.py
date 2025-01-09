from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from accounts.forms import PostForm
from accounts.models import Post

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  # Replace 'home' with your desired redirect URL
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/login.html')

@login_required
def user_profile(request):
    user_posts = Post.objects.filter(user=request.user)

    return render(request, 'accounts/profile.html', {'user':request.user, 'user_posts':user_posts})

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
