from asso_tn.utils import make_timed_token, token_valid

# from django.contrib import auth
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
# from django.http import HttpResponseServerError
from django.template.loader import render_to_string
# from django.urls import reverse
# from django.utils.encoding import force_bytes, force_text
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.crypto import get_random_string
# from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth.views import LoginView, LogoutView
# from django.conf import settings

from authentication.forms import RegistrationForm, AuthenticationForm, ProfileForm # SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from .models import Profile

"""
A quick note on the captcha:

1.  We should monitor it to know how often entities fail and how many
    attempts it requires to succeed.

2.  We should probably rate-limit the ability to response to captcha
    challenges.

3.  This article suggests that machines have become so good at
    responding to captchas that more human techniques are required.
    It proposes "add one to digits" as a test.  (This is consistent
    with the evolution of Google's recaptcha.)

    https://starcross.dev/blog/6/customising-django-simple-captcha/

4.  We don't use Google's recaptcha because we'd like to minimise data
    leaks to third parties, especially to GAFAs.

"""

def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            account = form.save()
            
            # Create account and login
            #TODO See to send registration confirm mail instead 
            # login(request, account)
            # return redirect("index")
            send_activation(request, account, True)
            return render(request, 'authentication/account_activation_sent.html', {'is_new': True})
            # return redirect('authentication:account_activation_sent', is_new=True)
        else:
            context["registration_form"] = form
    else:
        form = RegistrationForm()
        context["registration_form"] = form
    return render(request, "authentication/register.html", context)

def logout_view(request):
    logout(request)
    return redirect("index")

def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("index")

    if request.POST:
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]

            if password:
                user = authenticate(email=email, password=password)

                if not user.email_confirmed:
                    send_activation(request, user, True)
                    return render(request, "authentication/email_not_confirmed.html")

                if user:
                    login(request, user)
                    if not form.cleaned_data['remember_me']:
                        request.session.set_expiry(0)
                    return redirect("index")
            elif request.POST["mail_authentication"]:
                user = Profile.objects.get(email=form.cleaned_data['email'])

                if not user.email_confirmed:
                    send_activation(request, user, True)
                    return render(request, "authentication/email_not_confirmed.html")
                
                if not form.cleaned_data['remember_me']:
                        request.session.set_expiry(0)
                
                send_activation(request, user, False)
                return render(request, 'authentication/account_activation_sent.html', {'is_new': False})
                # return redirect('authentication:account_activation_sent', is_new=False)

                
    else:
        form = AuthenticationForm()
    
    context["login_form"] = form
    return render(request, "authentication/login.html", context)


# def login(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             try:
#                 user.refresh_from_db()
#                 if user.profile.authenticates_by_mail:
#                     send_activation(request, user)
#                     return redirect('authentication:account_activation_sent', is_new=False)
#             except ObjectDoesNotExist:
#                 print('ObjectDoesNotExist')
#                 pass            # I'm not sure this can ever happen.

#             # There should be precisely one or zero existing user with the
#             # given email, but since the django user model doesn't impose
#             # a unique constraint on user emails, I'm stuck verifying this.
#             existing_users = User.objects.filter(email=form.cleaned_data['email'])
#             if len(existing_users) > 1:
#                 return HttpResponseServerError(
#                     "Data error: Multiple email addresses found")
#             if len(existing_users) == 1:
#                 existing_user = existing_users[0]
#                 if existing_user.profile.authenticates_by_mail:
#                     send_activation(request, existing_user)
#                     return redirect('authentication:account_activation_sent', is_new=False)
#             user.email = form.cleaned_data['email']
#             user.username = get_random_string(20)
#             user.is_active = False
#             user.save()
#             send_activation(request, user)
#             return redirect('authentication:account_activation_sent', is_new=True)
#         else:
#             # Form is not valid.
#             pass
#     else:
#         form = SignUpForm()
#     return render(request, 'authentication/login.html', {'form': form})

def send_activation(request, user, is_new):
    """Send user an activation/login link.

    The caller should then redirect to / render a template letting the
    user know the mail is on its way, since the redirect is a GET.

    """
    current_site = get_current_site(request)
    subject = 'Votre compte à {dom}'.format(dom=current_site.domain)
    message = render_to_string('authentication/account_activation_email.html', {
        'user_id': user.pk,
        'domain': current_site.domain,
        'token': make_timed_token(user.pk, 20),
        "is_new": is_new,
    })
    recipient_list = [str(user.email)]
    send_mail(subject, "", None, recipient_list, fail_silently=False, html_message=message)
    # if hasattr(settings, 'ROLE') and settings.ROLE in ['staging', 'production']:
    #     user.email_user(subject, message)
    # else:
    #     # We're in dev.
    #     print("Mode dev : mél qui aurait été envoyé :")
    #     print(message)

# def account_activation_sent(request, is_new):
#     is_new_bool = is_new
#     return render(request, 'authentication/account_activation_sent.html', {'is_new': is_new_bool})

def activate(request, token):
    """Process an activation token.

    The result should be (1) to flag the user as having a valid email
    address and (2) to login the user.

    """
    user_id = token_valid(token)
    if user_id < 0:
        return render(request, 'authentication/account_activation_invalid.html')
    try:
        user = Profile.objects.get(pk=user_id)
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('index')
    except (TypeError, ValueError, OverflowError, Profile.DoesNotExist):
        return render(request, 'authentication/account_activation_invalid.html')

def profile_view(request):

    context = {}

    if not request.user.is_authenticated:
        return redirect("authenticate:login")

    if request.POST:
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(
            initial = { "email": request.user.email,
            "username": request.user.username}
        )
    context["profile_form"] = form
    return render(request, "authentication/profile.html", context)

# class DeauthView(LogoutView):
#     """Log out the user.

#     Renders the home page (but not by its view function, just via the
#     template, which is odd.  If the current page doesn't require
#     login, we should probably stay put, but that's neither important
#     now nor do I know how to do it.

#     """
#     template_name = "asso_tn/index.html"

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             # messages.success(request, f'Your Profile has been Updated Successfully')
#             return redirect('authentication:mod')
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)
#         context = {
#             'u_form': u_form,
#             'p_form': p_form
#         }
#     return render(request, 'authentication/profile.html', context)
