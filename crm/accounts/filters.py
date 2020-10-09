import django_filters

from .models import *

class OrderFilter(django_filters.FilterSet):

    start_date = django_filters.DateFilter(field_name="date_created", lookup_expr='gte')

    end_date = django_filters.DateFilter(field_name="date_created", lookup_expr='lte')

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']