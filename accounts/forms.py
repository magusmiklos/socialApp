from django import forms
from .models import Post, Profile

class PostForm(forms.ModelForm):
    class Meta:
       model = Post
       fields = ["title","text"]

    def save(self, commit=True):
        post = super().save(commit=False)
        post.user = self.request.user
        if commit:
            post.save()
        return post

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture','bio']
