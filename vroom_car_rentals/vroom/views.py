from django.http import HttpResponse
from django.shortcuts import render, redirect
from .functions import *

def index(request):
    return render(request, 'vroom/index.html')

def cars(request):
    cars = get_all_cars() # Retrieve all the cars and the relevant information (from functions.py)
    stores = Store.objects.values('name') # Retrieves the names of the stores
    make_name = Car.objects.values('make_name').order_by('make_name').distinct() # Retrieves all makes of cars from the database
    seriesYear = Car.objects.values('seriesYear').order_by('seriesYear').distinct() # Retrieves the years stored in the database
    fuel_system = Car.objects.values('fuel_system').order_by('fuel_system').distinct() # Retrieves the fuel systems stored in the database
    drive = Car.objects.values('drive').order_by('drive').distinct() # Retrieves the drive types stored in the database
    context = {'list_of_cars': cars, 'stores': stores, 'make_name': make_name, 'seriesYear': seriesYear, 'fuel_system': fuel_system, 'drive': drive} # Create a context dictionary that contains the retrieved cars and information used in filters
    
    if 'search' in request.GET: # The user has entered the cars page via the home site search or the cars page search bar
        filter = '%s' % request.GET.get('search') # Prepare a filter to apply to the cars retrieved
        cars = cars.filter(car__model__icontains=filter) # Filter the cars so that only ones with a similar model name appear

        filter_names = list() # Create a list to store the currently selected filter values
	
        if 'sort' in request.GET: # Sort the Results by Tank Capacity and determine sort input
            if request.GET.get('sort') == "Car_TankCapacity":
                context['sort'] = 'tank_high' # Set field to sort by to tank_high
                filter_names.append(request.GET.get('tank_high')) # Remember which drop-down item was used
                if request.GET.get('tank_high') == "high": # Sort By highest to lowest
                    cars = cars.extra({'tank_capacity':"tank_capacity + 0"}).order_by('-tank_capacity')
                else: # Sort By Lowest to highest
                    cars = cars.extra({'tank_capacity':"tank_capacity + 0"}).order_by('tank_capacity')

            elif request.GET.get('sort') == "Price_New": # Sort the Results by Price and determine sort input
                context['sort'] = 'price_high' # Set field to sort by to price_high
                filter_names.append(request.GET.get('price_high'))
                if request.GET.get('price_high') == "high": # Sort from highest to lowest
                    cars = cars.order_by('-car__price_new')
                else: # Sort from lowest to highest
                    cars = cars.order_by('car__price_new')

            elif request.GET.get('sort') == "Power": # Sort the Results by Power and determine sort input
                context['sort'] = 'power_high' # Set field to sort by to power_high
                filter_names.append(request.GET.get('power_high'))
                if request.GET.get('power_high') == "high": # Sort from highest to lowest
                    cars = cars.extra({'power':"power + 0"}).order_by('-power')
                else: # Sort from lowest to highest
                    cars = cars.extra({'power':"power + 0"}).order_by('power')

        if 'store' in request.GET and request.GET.get('store') != "":
            cars = cars.filter(return_store__name=request.GET.get('store'))
            filter_names.append(request.GET.get('store'))

        if 'make_name' in request.GET and request.GET.get('make_name') != "": # Apply the make filter if it is used when searching
            cars = cars.filter(car__make_name=request.GET.get('make_name')) # Filter the data to only show cars of the searched make name
            filter_names.append(request.GET.get('make_name')) # Add filter to list of selected filters
		
        if 'year' in request.GET and request.GET.get('year') != "": # Apply the year filter if it is used when searching
            cars = cars.filter(car__seriesYear=request.GET.get('year')) # Filter the data to only show cars of the searched year
            filter_names.append(int(request.GET.get('year'))) # Add filter to list of selected filters

        if 'fuel_system' in request.GET and request.GET.get('fuel_system') != "": # Apply the fuel_system filter if it is used when searching
            cars = cars.filter(car__fuel_system=request.GET.get('fuel_system')) # Filter the data to only show cars of the searched fuel system
            filter_names.append(request.GET.get('fuel_system')) # Add filter to the list of selected filters

        if 'drive' in request.GET and request.GET.get('drive') != "": # Apply the drive type filter if it is used when searching
            cars = cars.filter(car__drive=request.GET.get('drive')) # Filter the data to only show cars of the searched drive type
            filter_names.append(request.GET.get('drive')) # Add filter to the list of selected filters

        if len(filter_names) > 0:
            context['filter_names'] = filter_names
    
    else:
        cars = cars.filter(car__model__icontains='')

    context['list_of_cars'] = cars # Update the context with new results
		
    return render(request, 'vroom/cars.html', context)

def viewcustomers(request):
    users = get_all_customers() # Retrieve all the user information, from functions.py

    if 'search' in request.GET:
        filter = '%s' % request.GET.get('search') # Prepare a filter to apply to the users retrieved
        users = users.filter(name__icontains=filter) # Filter the users so that only ones with a similar model name appear

    else:
        users = users.filter(name__icontains='')

    context = {'list_of_users': users}

    return render(request, 'vroom/viewcustomers.html', context)

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

def stores(request):
    stores = Store.objects.values('name', 'address', 'phone')
    context = {'stores' : stores}
    return render(request, 'vroom/stores.html', context)

def storehistory(request):
    stores = get_all_stores() # Retrieve all the store information (from functions.py)
    context = {'list_of_stores': stores}

    if 'store' in request.GET:
        orders = get_all_orders() # Retrive all the order information (from functions.py)
        selected_store_id = int(request.GET.get('store')) # Retrieve the selected store from the html form
        for store in stores:
            if (store.store_id == selected_store_id): # If the store id is the same as the selected store, overide the store name to equal that of the selected store
                selected_store_name = store.name

        context = {'list_of_orders': orders, 'list_of_stores': stores, 'selected_store_id': selected_store_id, 'selected_store_name': selected_store_name}

    return render(request, 'vroom/storehistory.html', context) # Render the store history page with context
