
from django.urls import path
from .views import user_login, user_profile, user_logout, create_post

urlpatterns = [
    path('login/', user_login, name='login'),
    path('profile/', user_profile, name='profile'),
    path('logout/', user_logout, name='logout'),
    path('create_post', create_post, name='create_post'),
]
