from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from requests.exceptions import HTTPError
from social_django.utils import psa
from social_core.exceptions import AuthForbidden
from users.auth import CustomUserBackend
from users.serializers import FacultySerializer, StudentSerializer
from research.serializers import ResearchScholarSerializer

user_serializers = (FacultySerializer, ResearchScholarSerializer, StudentSerializer)


class SocialSerializer(serializers.Serializer):
    access_token = serializers.CharField(allow_blank=False, trim_whitespace=True)


def downcast_user(backend, user=None, *args, **kwargs):
    """Pipeline function to be used with PSA"""
    if user is None:  # Only allow users who have been previously added to db
        raise AuthForbidden(backend)
    downcasted_user = CustomUserBackend.downcast_user_type(user)
    if downcasted_user == user:
        raise AuthForbidden(backend)  # Don't allow CustomUser base model users
    return {"user": downcasted_user}


@api_view(["POST"])
@permission_classes([AllowAny])
@psa()
def exchange_token(request, backend):
    """Accept the Google OAuth Token from client flow and authenticate user."""
    serializer = SocialSerializer(data=request.data)
    if not serializer.is_valid(raise_exception=True):
        return
    try:
        user = request.backend.do_auth(serializer.validated_data["access_token"])
    except (HTTPError, AuthForbidden) as e:
        return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
    for serializer in user_serializers:
        if serializer.Meta.model is type(user):
            user_data = serializer(user).data
            break
    else:
        user_data = str(user)
    return Response({"user": user_data})
