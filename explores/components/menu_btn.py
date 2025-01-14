from operator import is_
from django_unicorn.components import UnicornView
from accounts.models import Follow
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

class MenuBtnView(UnicornView):
    user = None

    def mount(self):
        self.user = self.component_kwargs["user"]

    def toggle_follow(self):
        target_user = get_object_or_404(User,id=self.user.id)

        follow = Follow.objects.filter(follower=self.request.user,following=target_user).first()

        if follow != None:
            follow.delete()
            self.user.is_followed = False
        else:
            Follow.objects.create(follower=self.request.user,following=target_user)
            self.user.is_followed = True

        print(self.user.is_followed)
