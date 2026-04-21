from django.contrib.auth.models import AnonymousUser

from users.models import User


def get_user_name(*, user: User | AnonymousUser) -> str:
    """
    Provides the name of the user. It may be the login or
    the first name if specified.
    """
    if user.first_name:
        username = user.first_name
    else:
        username = user.username
    return username
