from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from requests.exceptions import HTTPError
from social_django.utils import psa
from social_core.exceptions import AuthForbidden
from users.serializers import FacultySerializer, StudentSerializer
from research.serializers import ResearchScholarSerializer

user_serializers = (FacultySerializer, ResearchScholarSerializer, StudentSerializer)


class SocialSerializer(serializers.Serializer):
    access_token = serializers.CharField(allow_blank=False, trim_whitespace=True)


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

    token = AccessToken.for_user(user)

    # serialize user data to be sent back to client
    for serializer in user_serializers:
        if serializer.Meta.model is type(user):
            token["role"] = user.__class__.__name__
            token["user"] = serializer(user).data
            del token["user"]['email']  # already sent in token
            break
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)  # Unknown User type
    return Response({"token": str(token)})
