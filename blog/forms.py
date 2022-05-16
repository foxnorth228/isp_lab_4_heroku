from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'autocomplete': 'off',
            'pattern': '[a-zA-Z0-9@.+-_]{1,150}',
            'title': 'Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.',
        })
        self.fields['password1'].widget.attrs.update({
            'autocomplete': 'off',
            'pattern': '(?=.*?[a-zA-Z])[a-zA-Z0-9]{8,}',
            'title': 'Enter a valid password.',
        })
        self.fields['password2'].widget.attrs.update({
            'autocomplete': 'off',
            'pattern': '(?=.*?[a-zA-Z])[a-zA-Z0-9]{8,}',
            'title': 'Enter a valid password.',
        })

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'tags')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text')

class AuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'autocomplete': 'off',
            'pattern': '[a-zA-Z0-9@.+-_]{1,150}',
            'title': 'Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.',
        })
        self.fields['password'].widget.attrs.update({
            'autocomplete': 'off',
            'pattern': '(?=.*?[a-zA-Z])[a-zA-Z0-9]{8,}',
            'title': 'Enter a valid password.',
        })
