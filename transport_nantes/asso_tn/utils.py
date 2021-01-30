import datetime

from django.conf import settings
from django.utils.crypto import salted_hmac
from django.utils.crypto import secrets
from django.utils.http import base36_to_int, int_to_base36

def make_timed_token(user_id, minutes, test_value_now=None):
    """Make a URL-safe timed token that's valid for minutes minutes.

    The token is tied to a specific user to avoid frauds where a token
    is used to validate a different user than the one intended (i.e.,
    to validate a user whose email the person doesn't control or by
    simple fishing for user id).

    The test_value_now is for testing and should not normally be set.

    """
    secret = settings.SECRET_KEY
    rand_value = secrets.token_urlsafe(20)
    if test_value_now is not None:
        now = test_value_now
    else:
        now = datetime.datetime.now().timestamp()
    soon_seconds = int_to_base36(int(now + 60 * minutes))
    hmac = salted_hmac(soon_seconds, rand_value + str(user_id)).hexdigest()[:20]
    return '{rnd}|{u}|{t}|{h}'.format(
        rnd=rand_value,
        u=user_id,
        t=soon_seconds,
        h=hmac)

def token_valid(timed_token, test_value_now=None):
    """Validate a timed token.

    Return the user id for which the token is valid, if the token is
    valid.  Return -1 if the token is not (either because it is
    malformed or because it has expired).

    The test_value_now is for testing and should not normally be set.

    """
    the_rand_value, the_user_id, the_soon, the_hmac = timed_token.split('|')
    computed_hmac = salted_hmac(the_soon, the_rand_value + str(the_user_id)).hexdigest()[:20]
    if computed_hmac != the_hmac:
        return -1
    if test_value_now is not None:
        now = test_value_now
    else:
        now = datetime.datetime.now().timestamp()
    if now > base36_to_int(the_soon):
        return -1
    return int(the_user_id)
