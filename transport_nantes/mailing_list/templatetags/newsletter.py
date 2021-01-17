from django import template
from mailing_list.forms import QuickMailingListSignupForm, QuickPetitionSignupForm

register = template.Library()

@register.inclusion_tag('mailing_list/panel/mailing_list.html')
def show_mailing_list():
    """Offer to join the mailing list.

    """
    form = QuickMailingListSignupForm
    return {'form': form}

@register.inclusion_tag('mailing_list/panel/one_mailing_list.html')
def show_one_mailing_list(list_name):
    """Offer to join a specific mailing list.

    The list_name is the mailing_list_token from the MailingList model.

    """
    form = QuickPetitionSignupForm
    return {'form': form,
            'list_name': list_name}
