from rest_framework_simplejwt.authentication import JWTAuthentication
from social_core.exceptions import AuthForbidden
from users.models import Faculty, Student
from research.models import ResearchScholar

user_models = (Faculty, ResearchScholar, Student)  # order is important


def downcast_user_type(user):
    """
    Retrieve the user from the first table that has a row with same email.
    Subclasses should be checked before parents.
    """
    if user is None:
        return None
    for Model in user_models:
        try:
            return Model.objects.get(email=user.email)
        except Model.DoesNotExist:
            pass
    return user  # fallback to base CustomUser model


class CustomJWTAuth(JWTAuthentication):
    def get_user(self, *args, **kwargs):
        return downcast_user_type(super().get_user(*args, **kwargs))


def downcast_social_user(backend, user=None, *args, **kwargs):
    """Pipeline function to be used with PSA"""
    if user is None:  # Only allow users who have been previously added to db
        raise AuthForbidden(backend)
    downcasted_user = downcast_user_type(user)
    if downcasted_user == user:
        raise AuthForbidden(backend)  # Don't allow CustomUser base model users
    return {"user": downcasted_user}
