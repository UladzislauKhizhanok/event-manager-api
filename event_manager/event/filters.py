import django_filters
from event import models


class EventFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name="start_date", lookup_expr="gte")
    end_date = django_filters.DateTimeFilter(field_name="end_date", lookup_expr="lte")
    type = django_filters.ChoiceFilter(field_name="type", choices=models.EventTypeEnum.choices)
    created_by = django_filters.CharFilter(field_name="created_by__username", lookup_expr="icontains")

    class Meta:
        model = models.Event
        fields = ["start_date", "end_date", "type", "created_by"]
