from django_filters import rest_framework as filters
from .models import Music


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class MusicFilter(filters.FilterSet):
    author = CharFilterInFilter(field_name='author', lookup_expr='in')
    genre = CharFilterInFilter(field_name='genre', lookup_expr='in')
    name = CharFilterInFilter(field_name='name', lookup_expr='in')

    class Meta:
        model = Music
        fields = ['author', 'genre', 'name']
