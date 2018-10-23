from django.http import HttpResponse
from django.shortcuts import render, redirect
from .functions import *
import re
import calendar

def index(request):
    return render(request, 'vroom/index.html')

def cars(request):
    cars = get_all_cars() # Retrieve all the cars and the relevant information (from functions.py)
    stores = Store.objects.values('name') # Retrieves the names of the stores
    make_name = Car.objects.values('make_name').order_by('make_name').distinct() # Retrieves all makes of cars from the database
    seriesYear = Car.objects.values('seriesYear').order_by('seriesYear').distinct() # Retrieves the years stored in the database
    fuel_system = Car.objects.values('fuel_system').order_by('fuel_system').distinct() # Retrieves the fuel systems stored in the database
    body_type = Car.objects.values('body_type').order_by('body_type').distinct() # Retrieves the different types of cars stored in the database
    seating_capacity = Car.objects.values('seating_capacity').order_by('seating_capacity').distinct() # Retrieves the seating_capacity stored in the database	
    drive = Car.objects.values('drive').order_by('drive').distinct() # Retrieves the drive types stored in the database
    filter = '' # Declare a string that'll be used for getting results by name
    context = {'list_of_cars': cars, 'filter': filter, 'stores': stores, 'make_name': make_name, 'seriesYear': seriesYear, 'fuel_system': fuel_system, 'body_type': body_type, 'seating_capacity': seating_capacity, 'drive': drive} # Create a context dictionary that contains the retrieved cars and information used in filters

    if 'search' in request.GET: # The user has entered the cars page via the home site search or the cars page search bar
        filter = '%s' % request.GET.get('search') # Prepare a filter to apply to the cars retrieved
        context['filter'] = filter # Update the context
        filter_names = list() # Create a list to store the currently selected filter values

        if 'sort' in request.GET: # Sort the Results by Tank Capacity and determine sort input
            if request.GET.get('sort') == "Car_TankCapacity":
                context['sort'] = 'tank_high' # Set field to sort by to tank_high
                filter_names.append(request.GET.get('tank_high')) # Remember which drop-down item was used
                if request.GET.get('tank_high') == "high": # Sort By highest to lowest
                    cars = cars.extra({'tank_capacity': "tank_capacity + 0"}).order_by('-tank_capacity')
                else: # Sort By Lowest to highest
                    cars = cars.extra({'tank_capacity': "tank_capacity + 0"}).order_by('tank_capacity')

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
                    cars = cars.extra({'power': "power + 0"}).order_by('-power')
                else: # Sort from lowest to highest
                    cars = cars.extra({'power': "power + 0"}).order_by('power')

        # Iterates through an array of names and parameters to apply filters.
        filters = [['store', 'return_store__name'], ['make_name', 'car__make_name'], ['year', 'car__seriesYear'],
                      ['fuel_system', 'car__fuel_system'], ['body_type', 'car__body_type'], ['drive', 'car__drive'],
                      ['seating_capacity', 'car__seating_capacity']]
        for name, parameter in filters:
            if name in request.GET and request.GET.get(name) != "":
                cars = cars.filter(**{parameter: request.GET.get(name)}) # Set the parameter to be whatever value is retrieved
                if name not in ('year', 'seating_capacity'):
                    filter_names.append(request.GET.get(name))
                else:
                    filter_names.append(int(request.GET.get(name)))

        if len(filter_names) > 0:
            context['filter_names'] = filter_names

    cars = cars.filter(car__model__icontains=filter) # Filter the cars so that only ones with a similar model name appear
    context['list_of_cars'] = cars # Update the context with new results

    return render(request, 'vroom/cars.html', context)

def viewcustomers(request):
    users = get_all_customers() # Retrieve all the user information, from functions.py

    if 'search' in request.GET:
        filter = '%s' % request.GET.get('search') # Prepare a filter to apply to the users retrieved
    else:
        filter = ''

    users = users.filter(name__icontains=filter) # Filter the users so that only ones with a similar model name appear
    context = {'list_of_users': users, 'filter': filter}

    return render(request, 'vroom/viewcustomers.html', context)

def login(request):
    if 'id' in request.POST and 'password' in request.POST: # The user has entered the login site by entering their login details
        id = request.POST.get('id') # Get the input id
        password = request.POST.get('password') # Get the input password (from login form)

        if authenticate_user(id, password): # Check that the user exists in the table
            user_information = get_user_info(id, password) # Get the name and access of the user
            request.session['username'] = user_information['username'] # Create a session variable for their name
            request.session['access'] = user_information['access'] # Create a session variable for their access
            request.session['id'] = id # Create a session variable for their id

            return redirect('vroom:index') # Redirect the user back to the home page

        context = {'id': id, 'password': password} # The users information was not found in the database
        return render(request, 'vroom/log-in.html', context) # Render the login page again (will now have their details auto-filled and a message)

    return render(request, 'vroom/log-in.html') # Render the login page for the first time

def logout(request):
    if request.session['username'] and request.session['access']: # Make sure the session variables are created
        del request.session['username'] # Remove the session variable
        del request.session['access'] # Remove the session variable

        request.session.modified = True # Ensure django knows the session variables were modified

    return redirect('vroom:index') # Redriect the user to the home page

def stores(request):
    stores = Store.objects.values('name', 'address', 'phone')
    context = {'stores': stores}
    return render(request, 'vroom/stores.html', context)

def storehistory(request):
    orders = get_all_orders() # Retrive all the order information (from functions.py)
    stores = get_all_stores() # Retrieve all the store information (from functions.py)
    try: # A failure occurs when no one is logged in (accessing via search bar)
        if request.session['access'] == "CUSTOMER": # This is the line that fails
            orders = orders.filter(customer_id=request.session['id'])

            
        context = {'list_of_stores': stores, 'table_data': {'Orders': orders}}
        
        context = {'list_of_orders' : orders, 'table_data': {'Orders': orders}}
                

        orders = orders.filter(customer_id=request.session['id'])
        context = {'list_of_stores': stores, 'table_data': {'Orders': orders}} 
        if 'store' in request.GET and not 'clear' in request.GET:
            selected_store_id = int(request.GET.get('store')) # Retrieve the selected store id from the html form
            pickup_stores = orders.filter(pickup_store=selected_store_id)
            return_stores = orders.filter(return_store=selected_store_id)
            selected_store_name = stores.get(store_id=selected_store_id).name # Retrieve the name that belongs to the ID
            pickup_order_table_name = 'Pickup Orders:'
            return_order_table_name = 'Return Orders:'

            if len(pickup_stores) == 0: # If there aren't any values in pickup_stores and/or return_stores, set the respective title to have 'No' at the begining
                pickup_order_table_name = 'No Pickup Orders'
            if len(return_stores) == 0:
                return_order_table_name = 'No Return Orders'

            context = {
                'customer_orders': orders,
                'list_of_stores': stores,
                'table_data': {pickup_order_table_name: pickup_stores, return_order_table_name: return_stores}, # Used for simplifying the code in storehistory.html
                'selected_store_name': selected_store_name,
                'selected_store_id': selected_store_id
            }
     
    except KeyError: #Prevent a user that isn't logged in frm viewing anything upon failure
        context = {'list_of_stores': stores, 'table_data': {"You don't have permission to view this page.": None}}

    return render(request, 'vroom/storehistory.html', context) # Render the store history page with context

def analytics(request):
    # Minimum and maximum date for the report month selector
    min_date = "%d-%02d" % (get_min_order_date()['min_date'].year, get_min_order_date()['min_date'].month)
    max_date = "%d-%02d" % (get_max_order_date()['max_date'].year, get_max_order_date()['max_date'].month)

    context = {'min_date': min_date, 'max_date': max_date}

    date_expression = re.compile('^[0-9]{4}-[0-9]{2}$') # Regex to check date input

    if 'report' in request.GET and date_expression.match(request.GET.get('report')): # Ensure get request exists and is correct date format
        date = request.GET.get('report') # Get requested month

        report = generate_report(int(date[:4]), int(date[-2:])) # Get report information

        # Fill report information into context
        context['report'] = report
        context['selected_date'] = date
        context['selected_date_text'] = calendar.month_name[int(date[-2:])] + ', ' + date[:4] # String version of month (e.g July, 2005)


    return render(request, 'vroom/analytics.html', context)
