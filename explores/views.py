from django.contrib.auth.views import login_required
from django.shortcuts import render, get_object_or_404
from django.core.serializers.base import ObjectDoesNotExist
from django.contrib.auth.models import User
from accounts.models import Post,Profile
from django.core.paginator import Paginator
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
    for post in posts:
        post.text = post.text.replace('\n', '<br>')

    posts_with_user = [(post, post.user) for post in posts]

    paginator = Paginator(posts_with_user, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'explores/explore.html', {'page_obj':page_obj, 'search_query':search_query, })

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

@login_required
def follow_view(request):
    return render(request,"explores/follow.html")

@login_required
def people_view(request):
    search_query = request.GET.get('search', '')

    if search_query:
        users = User.objects.select_related('profile').filter(
            username__icontains=search_query
        )
    else:
        users = User.objects.select_related('profile').all()

    for user in users:
        if user.profile.bio == None:
            break
        elif len(user.profile.bio) > 20:
            user.profile.bio = user.profile.bio[:20] + '...'

    paginator = Paginator(users, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "explores/people.html", {"page_obj": page_obj, "search_query": search_query})
