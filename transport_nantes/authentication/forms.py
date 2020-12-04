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
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe", required= False)
    mail_authentication = forms.BooleanField(required=False, label="Identification sans mot de passe", initial=False)

    class Meta:
        model = Profile
        fields = ("email", "password", "mail_authentication")

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data["email"]
            if self.cleaned_data["password"]:
                password = self.cleaned_data["password"]
                if not authenticate(email=email, password=password):
                    raise forms.ValidationError("Email ou mot de passe invalide")
            elif self.cleaned_data["mail_authentication"]:
                pass
            else:
                raise forms.ValidationError("Veuillez soit entrer un mot de passe, soit cocher la case \"Identification sans mot de passe\"")


class ProfileForm(forms.ModelForm):
    
    username = forms.CharField(label="Nom d'utilisateur")

    class Meta:
        model = Profile
        fields = ("email", "username",)

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data["email"]
            try:
                account = Profile.objects.exclude(pk= self.instance.pk).get(email=email)
            except Profile.DoesNotExist:
                return email
            raise forms.ValidationError("L\'email '%s' est déjà utilisé. \nVeuillez l\'orthographe ou que vous n\'avez pas un compte associé à cette adresse" % account.email)

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data["username"]
            try:
                account = Profile.objects.exclude(pk= self.instance.pk).get(username=username)
            except Profile.DoesNotExist:
                return username
            raise forms.ValidationError("Le nom '%s' est déjà utilisé." % account.username)


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
