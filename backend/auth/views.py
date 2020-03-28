from requests.exceptions import HTTPError
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from social_core.exceptions import AuthForbidden
from social_django.utils import psa
from users.serializers import user_serializers


class SocialSerializer(serializers.Serializer):
    access_token = serializers.CharField(allow_blank=False, trim_whitespace=True)


def get_token_for_user(user):
    token = AccessToken.for_user(user)

    # serialize user data to be sent back to client
    for serializer in user_serializers:
        if serializer.Meta.model is type(user):
            token["role"] = user._meta.verbose_name
            if getattr(user, "is_hod", False):
                token["role"] = "hod"
            token["user"] = serializer(user).data
            del token["user"]["email"]  # already sent in token
            return token


@api_view(["POST"])
@permission_classes([AllowAny])
@psa()
def exchange_token(request, backend):
    """Accept the Google OAuth Token from client flow and authenticate user."""
    serializer = SocialSerializer(data=request.data)
    if not serializer.is_valid(raise_exception=True):  # validate access_token
        return
    try:
        user = request.backend.do_auth(serializer.validated_data["access_token"])
    except (HTTPError, AuthForbidden) as e:
        return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    token = get_token_for_user(user)
    if not token:
        return Response(status=status.HTTP_400_BAD_REQUEST)  # Unknown User type
    return Response({"token": str(token)})
