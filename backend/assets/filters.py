import django_filters
from .models import Asset


class AssetFilter(django_filters.FilterSet):
    """
    Filter class for Asset model to enable search and filtering
    """
    # Search by title (case-insensitive, partial match)
    title = django_filters.CharFilter(lookup_expr='icontains')

    # Search by description (case-insensitive, partial match)
    description = django_filters.CharFilter(lookup_expr='icontains')

    # Search by tags (case-insensitive, partial match)
    tags = django_filters.CharFilter(lookup_expr='icontains')

    # Filter by file type
    file_type = django_filters.CharFilter(lookup_expr='iexact')

    # Filter by date range
    created_at_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    # General search across multiple fields
    search = django_filters.CharFilter(method='search_filter')

    class Meta:
        model = Asset
        fields = ['title', 'description', 'tags', 'file_type', 'created_at_after', 'created_at_before']

    def search_filter(self, queryset, name, value):
        """
        Custom filter method for searching across multiple fields
        """
        return queryset.filter(
            models.Q(title__icontains=value) |
            models.Q(description__icontains=value) |
            models.Q(tags__icontains=value)
        )


from django.db import models