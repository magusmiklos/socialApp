from django.contrib.auth.views import login_required
from django.shortcuts import render, get_object_or_404
from django.core.serializers.base import ObjectDoesNotExist
from django.contrib.auth.models import User
from accounts.models import Post,Profile
import profile

@login_required
def explore_view(request):
    search_query = request.GET.get('search','')
    if search_query:
        posts = Post.objects.filter(
            title__icontains=search_query
        ) | Post.objects.filter(
            text__icontains=search_query
        )
    else:
        posts = Post.objects.all()
    posts = posts.order_by('-created_at')

    posts_with_user = [(post, post.user) for post in posts]
    return render(request,'explores/explore.html', {'posts_with_user':posts_with_user, 'search_query':search_query, })

@login_required
def check_out_profile(request, id):
    user = get_object_or_404(User,id=id)

    profile = user.profile

    user_posts = Post.objects.filter(user=user).order_by('-created_at')

    return render(request,"explores/check_out_profile.html", {'user':user, 'user_posts':user_posts, 'profile':profile})

@login_required
def check_out_post(request,id):

    post = get_object_or_404(Post,id=id)

    user = post.user

    return render(request,"explores/check_out_post.html",{"post":post,"user":user})
