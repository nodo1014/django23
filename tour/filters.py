import django_filters

from .models import *

class ItemFilter(django_filters.FilterSet):
    class Meta:
        model = TourItem
        fields = '__all__'
        