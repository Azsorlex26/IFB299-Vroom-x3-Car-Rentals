from django.http import HttpResponse
from django.shortcuts import render, redirect
from .functions import *

def index(request):
    return render(request, 'vroom/index.html')

def cars(request):
    if 'search' in request.GET: # The user has entered the cars page via the home site search
        cars = get_all_cars() # Retrieve all the cars and the relevant information (from functions.py)
        filter = '%s' % request.GET.get('search') # Prepare a filter to apply to the cars retrieved
        cars_by_name = cars.filter(car__model__icontains=filter) # Filter the cars so that only ones with a similar model name appear

        context = {'list_of_cars': cars_by_name} # Create a context dictionary that contains the retrieved and filtered cars

        return render(request, 'vroom/cars.html', context) # Render the cars page with the context included
    else: # The user has entered the cars page without entering any search
        return render(request, 'vroom/cars.html')

def login(request):
    if 'id' in request.POST and 'password' in request.POST: # The user has entered the login site by entering their login details
        id = request.POST.get('id') # Get the input id
        password = request.POST.get('password') # Get the input password (from login form)
        if authenticate_user(id, password): # Check that the user exists in the table
            user_information = get_user_info(id, password) # Get the name and access of the user

            request.session['username'] = user_information['username'] # Create a session variable for their name
            request.session['access'] = user_information['access'] # Create a session variable for their access

            return redirect('vroom:index') # Redirect the user back to the home page
        else: # The users information was not found in the database
            context = {'id': id, 'password': password} # Create a context of the information they sent

            return render(request, 'vroom/log-in.html', context) # Render the login page again (will now have their details auto-filled and a message)
    else: # This is the first time they are accessing the login page
        return render(request, 'vroom/log-in.html') # Render the login page for the first time

def logout(request):
    if request.session['username'] and request.session['access']: # Make sure the session variables are created
        del request.session['username'] # Remove the session variable
        del request.session['access'] # Remove the session variable

        request.session.modified = True # Ensure django knows the session variables were modified

    return redirect('vroom:index') # Redriect the user to the home page
