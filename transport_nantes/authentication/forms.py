from django import forms
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField
from .models import Profile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=150, label="Adresse email", help_text="Obligatoire")
    username = forms.CharField(max_length=50, label="Nom d'utilisateur", help_text="Obligatoire")
    captcha = CaptchaField(help_text="Obligatoire", error_messages=dict(invalid="Captch incorrect, veuillez réessayer"))
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=128, label="Mot de passe", help_text="Obligatoire")
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=128, label="Confirmation du mot de passe", help_text="Obligatoire")

    class Meta:
        model = Profile
        fields = ("email", "username", "password1", "password2", "captcha")


# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(
#         max_length=254,
#         label="Adresse mél", help_text='Obligatoire')
#     captcha = CaptchaField(
#         help_text='Obligatoire',
#         error_messages=dict(invalid="captcha incorrect, veuillez réessayer"))
#     password1 = forms.CharField(
#         widget=forms.PasswordInput, max_length=254,
#         label="Mot de passe", required=False,
#         help_text="Facultatif")
#     password2 = forms.CharField(
#         widget=forms.PasswordInput, max_length=254,
#         label="Mot de passe", required=False,
#         help_text="Encore la même chose")

#     class Meta:
#         model = User
#         fields = ('email', 'password1', 'password2', )

# class UserUpdateForm(forms.ModelForm):
#     email = forms.EmailField(label="Adresse mél")

#     class Meta:
#         model = User
#         fields = ['email']

# class ProfileUpdateForm(forms.ModelForm):
#     display_name = forms.CharField(label="Nom d'affichage")

#     class Meta:
#         model = Profile
#         fields = ['display_name']
