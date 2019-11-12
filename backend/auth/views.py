from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from requests.exceptions import HTTPError
from social_django.utils import psa
from social_core.exceptions import AuthForbidden


class SocialSerializer(serializers.Serializer):
    access_token = serializers.CharField(allow_blank=False, trim_whitespace=True)


@api_view(["POST"])
@permission_classes([AllowAny])
@psa()
def exchange_token(request, backend):
    serializer = SocialSerializer(data=request.data)
    if not serializer.is_valid(raise_exception=True):
        return
    try:
        user = request.backend.do_auth(serializer.validated_data["access_token"])
    except (HTTPError, AuthForbidden) as e:
        return Response({"error": str(e)}, status=403)
    return Response({"user": str(user)})
