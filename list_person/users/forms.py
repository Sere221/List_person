from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserOurRegistraion(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']


class ProfileImage(forms.ModelForm):

    def __init__(self, *args, **kwards):
        super(ProfileImage, self).__init__(*args, **kwards)
        self.fields['images'].label = "Изображение сотрудника"

    class Meta:
        model = Profile
        fields = ['name', 'slug', 'images', 'account_type', 'filial', 'department', 'salary']


class ProfileImageDis(forms.ModelForm):

    def __init__(self, *args, **kwards):
        super(ProfileImageDis, self).__init__(*args, **kwards)
        self.fields['images'].label = "Изображение сотрудника"
        for field in self.fields.values():
            field.disabled = True

    class Meta:
        model = Profile
        fields = ['name', 'slug', 'images', 'account_type', 'filial', 'department', 'salary']