from django.urls import path
from .views import check_out_post, explore_view, check_out_profile, follow_view, people_view, followed_people_view

urlpatterns = [
    path('',explore_view, name='explore'),
    path('check_out_profile/<int:id>/', check_out_profile, name='check_out_profile'),
    path('check_out_post/<int:id>/', check_out_post, name='check_out_post'),
    path('follow/', follow_view, name='follow'),
    path('people/', people_view, name='people'),
    path('followed/',followed_people_view, name='followed')
]
