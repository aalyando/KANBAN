from .models import Task
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class FormCreate(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'created_by']


class AuthenticationForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(label=("Password"), widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user is None:
                raise forms.ValidationError("Invalid username or password")

            cleaned_data['authenticated_user'] = user

        return cleaned_data


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)

        if not (self.user and self.user.is_superuser):
            del self.fields['assigned_to']

