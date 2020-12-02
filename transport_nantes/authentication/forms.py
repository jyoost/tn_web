from django import forms
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField
from .models import Profile
from django.contrib.auth import authenticate


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=150, label="Adresse email", help_text="Obligatoire")
    username = forms.CharField(max_length=50, label="Nom d'utilisateur", help_text="Obligatoire")
    captcha = CaptchaField(help_text="Obligatoire", error_messages=dict(invalid="Captch incorrect, veuillez réessayer"))
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=128, label="Mot de passe", help_text="Obligatoire")
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=128, label="Confirmation du mot de passe", help_text="Obligatoire")

    class Meta:
        model = Profile
        fields = ("email", "username", "password1", "password2", "captcha")


class AuthenticationForm(forms.ModelForm):
    email = forms.EmailField(label="Adresse email")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

    class Meta:
        model = Profile
        fields = ("email", "password")

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data["email"]
            password = self.cleaned_data["password"]
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Email ou mot de passe invalide")

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
