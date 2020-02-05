from django.db.models import Q
from django.http import Http404
from rest_framework_extensions.mixins import NestedViewSetMixin as _NestedViewSetMixin


class NestedViewSetMixin(_NestedViewSetMixin):
    """Add support for __or__ queries in fields"""

    def filter_queryset_by_parents_lookups(self, queryset):
        parents_query_dict = self.get_parents_query_dict()
        if parents_query_dict:
            query = Q()
            for lookup, value in parents_query_dict.items():
                if "__or__" in lookup:
                    lookups = lookup.split("__or__")
                    query &= Q(_connector=Q.OR, **dict.fromkeys(lookups, value))
                else:
                    query &= Q(**{lookup: value})
            try:
                return queryset.filter(query)
            except ValueError:
                raise Http404
        else:
            return queryset
