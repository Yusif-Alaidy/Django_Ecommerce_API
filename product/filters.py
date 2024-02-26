import django_filters
from product.models import *

class ProductFilter(django_filters.FilterSet):
    name     = django_filters.CharFilter           (lookup_expr='iexact')
    Keyword  = django_filters.filters.CharFilter   (field_name='name', lookup_expr='icontains')
    minPrice = django_filters.filters.NumberFilter (field_name="price" or 0, lookup_expr='gte')
    maxPrice = django_filters.filters.NumberFilter (field_name="price" or 10000, lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['price', 'name']