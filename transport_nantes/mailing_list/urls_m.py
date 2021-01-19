from django.urls import path
from django.conf import settings
from .views_m import *
from asso_tn.views import AssoView
from .forms import QuickPetitionSignupForm

app_name = 'mailing_list'
urlpatterns = [
    path('inscrire', MailingListSignupM.as_view(), name='list_signup'),
    path('inscrire-captcha', QuickMailingListSignupM.as_view(), name='quick_list_signup'),
    path('petition-captcha', QuickMailingListSignupM.as_view(), name='quick_petition_signup'),
    path('petition/<slug:petition>/', AssoView.as_view(
        template_name='mailing_list/petitions/pays-de-la-loire-2021.html'),
         {'form': QuickPetitionSignupForm(initial={'petition': petition})},
         name='petition')
]

# For debugging the thankyou template:
if hasattr(settings, 'ROLE') and 'production' != settings.ROLE:
    urlpatterns.append(path('merci', MailingListMerciM.as_view(), name='list_ok'))
