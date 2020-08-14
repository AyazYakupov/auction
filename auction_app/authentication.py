from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _


class CustomTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        credentials = super().authenticate(request)
        if not credentials:
            msg = _('Authorization header is empty.')
            raise AuthenticationFailed(msg)
        return credentials
