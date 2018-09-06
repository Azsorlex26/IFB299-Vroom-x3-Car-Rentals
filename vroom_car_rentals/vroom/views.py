from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'vroom/index.html')

def cars(request):
    if 'search' in request.GET:
        context = {'something': 'something'}
        return render(request, 'vroom/cars.html', context)
    else:
        message = "You didn't submit anything"
        return render(request, 'vroom/cars.html')
