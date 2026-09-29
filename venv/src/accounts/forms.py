from django import forms
from django.contrib.auth.models import User
from .models import Profile,Post,Comment


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError('Passwords do not match. ')

        return cleaned_data

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content','category']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']