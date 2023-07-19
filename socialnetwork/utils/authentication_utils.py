from rest_framework.authentication import BaseAuthentication
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from django.contrib.auth import authenticate, get_user_model


def get_authorization_header(request):
    """
    Return request's 'email, password' header
    """
    auth_email = request.META.get('HTTP_EMAIL')
    auth_password = request.META.get('HTTP_PASSWORD')
    return auth_email, auth_password


class CustomBasicAuthentication(BaseAuthentication):
    """
    HTTP Custom Basic authentication against email/password.
    """

    def authenticate(self, request):
        """
        Returns a `User` if a correct email and password have been supplied
        using HTTP Basic authentication.  Otherwise returns `None`.
        """
        auth_email, auth_password = get_authorization_header(request)

        if not auth_email:
            msg = _('Invalid basic header. No username provided in header.')
            raise exceptions.AuthenticationFailed(msg)
        elif not auth_password:
            msg = _('Invalid basic header. No Password is provided in header.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(auth_email, auth_password, request)

    def authenticate_credentials(self, email, password, request=None):
        """
        Authenticate the customer against provided email and password.
        """
        credentials = {
            get_user_model().USERNAME_FIELD: email,
            'password': password
        }
        user = authenticate(request=request, **credentials)

        if user is None:
            raise exceptions.AuthenticationFailed(_('Invalid username/password.'))

        if not user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return user, None
