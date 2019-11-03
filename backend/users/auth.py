from django.contrib.auth.backends import ModelBackend
from .models import Faculty, Student
from research.models import ResearchScholar


class CustomUserBackend(ModelBackend):
    """
    Backend that tries to "downcast" the user into proper subclass.

    To ensure that the `request.user` property has all the fields of the logged in
    user, this model backend returns objects of the subclass instead of CustomUser.
    """

    user_models = (Faculty, ResearchScholar, Student)  # order is important

    def authenticate(self, *args, **kwargs):
        return self.downcast_user_type(super().authenticate(*args, **kwargs))

    def get_user(self, *args, **kwargs):
        return self.downcast_user_type(super().get_user(*args, **kwargs))

    def downcast_user_type(self, user):
        """
        Retrieve the user from the first table that has a row with same email.
        Subclasses should be checked before parents.
        """
        for Model in self.user_models:
            try:
                return Model.objects.get(email=user.email)
            except Model.DoesNotExist:
                pass
        return user  # fallback to base CustomUser model
