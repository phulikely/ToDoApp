import django_filters
from django_filters.filters import CharFilter

from .models import Task

class TaskFilter(django_filters.FilterSet):
    name = CharFilter(field_name='title', lookup_expr='icontains')
    # class Meta:
    #     model = Task