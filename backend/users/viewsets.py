from rest_framework import viewsets, mixins
from .permissions import IsFaculty, IsSelf, IsFacultyOrIsSelf


class UserViewset(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    def get_permissions(self):
        permission_classes = []
        if self.action == "list":
            permission_classes = [IsFaculty]
        elif self.action == "retrieve":
            permission_classes = [IsFacultyOrIsSelf]
        else:  # update actions
            permission_classes = [IsSelf]
        return [perm() for perm in permission_classes]
