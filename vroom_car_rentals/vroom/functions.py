from .models import *
from django.db.models import Max

def get_all_cars():
    dates = Order.objects.values('car').annotate(max_date=Max('return_date')).values('max_date')
    cars = Order.objects.select_related('car', 'return_store').filter(return_date__in=dates)

    return cars
