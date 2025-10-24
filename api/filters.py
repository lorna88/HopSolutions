from django_filters import FilterSet, DateFilter, CharFilter

from tasks.models import Task


class TaskFilter(FilterSet):
    date_after = DateFilter(field_name='date', lookup_expr='gte')
    date_before = DateFilter(field_name='date', lookup_expr='lte')
    category = CharFilter(field_name='category__name', lookup_expr='icontains')
    tag = CharFilter(field_name='tags__name', lookup_expr='icontains')

    class Meta:
        model = Task
        fields = ['date', 'date_after', 'date_before', 'is_completed', 'category', 'tag']