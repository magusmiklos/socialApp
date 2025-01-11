
from django.urls import path
from .views import user_login, user_profile, user_logout, create_post, load_post, delete_post, edit_profile, user_register

urlpatterns = [
    path('login/', user_login, name='login'),
    path('profile/', user_profile, name='profile'),
    path('logout/', user_logout, name='logout'),
    path('create_post/', create_post, name='create_post'),
    path('post_detail/<int:id>/', load_post, name='post_detail'),
    path('delete_post/<int:id>/', delete_post, name='delete_post'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('register/', user_register, name='register'),
]
