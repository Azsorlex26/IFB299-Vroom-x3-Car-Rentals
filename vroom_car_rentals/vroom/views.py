from django.http import HttpResponse
from django.shortcuts import render
from .functions import *

def index(request):
    return render(request, 'vroom/index.html')

def cars(request):
    if 'search' in request.GET:
        cars = get_all_cars()
        filter = '%s' % request.GET.get('search')
        cars_by_name = cars.filter(car__model__icontains=filter)
        context = {'list_of_cars': cars_by_name}
        return render(request, 'vroom/cars.html', context)
    else:
        message = "You didn't submit anything"
        return render(request, 'vroom/cars.html')
