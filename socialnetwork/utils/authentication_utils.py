import base64
import binascii

from rest_framework.authentication import BaseAuthentication, BasicAuthentication
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, HTTP_HEADER_ENCODING
from django.contrib.auth import authenticate, get_user_model


class CustomAuthentication(BaseAuthentication):
    """
    HTTP Custom Basic authentication against email/password.
    """

    def get_authorization_header(self, request):
        """
        Return request's 'email, password' header
        """
        auth_email = request.META.get('HTTP_EMAIL')
        auth_password = request.META.get('HTTP_PASSWORD')
        return auth_email, auth_password

    def authenticate(self, request):
        """
        Returns a `User` if a correct email and password have been supplied
        using HTTP Basic authentication.  Otherwise returns `None`.
        """
        auth_email, auth_password = self.get_authorization_header(request)

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
            get_user_model().USERNAME_FIELD: email.lower(),
            'password': password
        }
        user = authenticate(request=request, **credentials)

        if user is None:
            raise exceptions.AuthenticationFailed(_('Invalid username/password.'))

        if not user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return user, None


class CustomBasicAuthentication(BaseAuthentication):
    """
    HTTP Custom Basic authentication against email/password.
    """

    def get_authorization_header(self, request):
        """
        Return request's 'Authorization:' header, as a bytestring.

        Hide some test client ickyness where the header can be unicode.
        """
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        if isinstance(auth, str):
            # Work around django test client oddness
            auth = auth.encode(HTTP_HEADER_ENCODING)
        return auth

    def authenticate(self, request):
        """
        Returns a `User` if a correct username and password have been supplied
        using HTTP Basic authentication. Otherwise returns `None`.
        """
        auth = self.get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'basic':
            return None

        if len(auth) == 1:
            msg = _('Invalid basic header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid basic header. Credentials string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            try:
                auth_decoded = base64.b64decode(auth[1]).decode('utf-8')
            except UnicodeDecodeError:
                auth_decoded = base64.b64decode(auth[1]).decode('latin-1')
            auth_parts = auth_decoded.partition(':')
        except (TypeError, UnicodeDecodeError, binascii.Error):
            msg = _('Invalid basic header. Credentials not correctly base64 encoded.')
            raise exceptions.AuthenticationFailed(msg)

        userid, password = auth_parts[0], auth_parts[2]
        return self.authenticate_credentials(userid, password, request)

    def authenticate_credentials(self, userid, password, request=None):
        """
        Authenticate the userid and password against username and password
        with optional request for context.
        """
        credentials = {
            get_user_model().USERNAME_FIELD: userid.lower(),
            'password': password
        }
        user = authenticate(request=request, **credentials)

        if user is None:
            raise exceptions.AuthenticationFailed(_('Invalid username/password.'))

        if not user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return (user, None)
