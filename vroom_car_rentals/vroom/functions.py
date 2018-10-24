from .models import *
from django.db.models import Max, Sum, Count, Q, Min
import calendar

def get_all_cars():
    # Retrieves all information about cars as well as the store they are in (the last store they were dropped off to in orders)

    # Sub query used to retrieve the most recent order id for a car (LIMIT 1 ensures only 1 value is returned)
    recent_order_per_car = 'vroom_order.order_id = (SELECT g.order_id FROM vroom_order g WHERE g.car_id = vroom_order.car_id ORDER BY g.return_date DESC LIMIT 1)'

    # Join the order, car and store tables on the car_id = car_id and return_store_id = store_id
    cars = Order.objects.select_related('car', 'return_store')

    # Filter the results so each car is unique
    cars = cars.extra(where={recent_order_per_car})

    return cars

def get_all_orders():
    # Retrieves all information about orders

    orders = Order.objects.all()

    return orders

def get_all_stores():
    # Retrieves all information about stores

    stores = Store.objects.all()

    return stores

def get_all_customers():
    # Retrieves all information about customers

    customers = User.objects.all()

    return customers

def authenticate_user(check_id, check_password):
    # Checks to see if the user exists in the database

    users = get_user(check_id, check_password);

    return users; #True if a user was found. False if not

def get_user_info(check_id, check_password):
    # Gets the name and role name for the specific user (assumes the id and password exists in the database)

    users = get_user(check_id, check_password);

    user = users[0] # Only take the first instance (okay to do since we are retrieving users by a specific id [the primary key] so there can only be 1)

    access = Role.objects.filter(role_id=user.role_id) # Get the access object for the user

    return {'username': user.name, 'access': access[0].name} # Return a dicitonary with their username and access name

def get_user(check_id, check_password):
    # Searches for the user in the database and returns the result of the query

    password_filter = ["password = SHA2(CONCAT('%s', salt), 0)" % check_password] # Filter to access the users password
    users = User.objects.filter(user_id=check_id).extra(where=password_filter) # Apply the password filter to see if any users have the password they entered (and has the specific id)

    return users

def get_min_order_date():
    # Returns the minimum order creation date in the order table
    return get_all_orders().aggregate(min_date=Min('create_date'))

def get_max_order_date():
    # Returns the maximum return date in the orders table
    return get_all_orders().aggregate(max_date=Max('return_date'))

def get_money(year, month):
    # Gets the total money earned in a selected month

    CAR_PRICE_PROFIT = 0.2 # Percentage the company earns from a car

    # Select all the orders for a specific year and month, and sum the price of each car that was in an order at that time
    money = get_all_orders().select_related().filter(pickup_date__year=year, pickup_date__month=month).aggregate(money=Sum('car__price_new'))

    if (money['money'] is None): # Check if no orders happened in the month
        money = 0
    else:
        money = money['money'] * CAR_PRICE_PROFIT # Store only makes 20% of that profit

    return money

def get_store_activity(year, month):
    # Gets the number of pickup and returns from each store in a specific month

    # Get all the stores and have room for the pickup, return and total counters
    stores = get_all_stores().values('store_id', 'name').annotate(pickup_activity=Count('store_id'), return_activity=Count('store_id'), total_activity=Count('store_id')) # Get a queryset of all stores

    # Get a queryset of each stores (pickup counts and returns)
    pickup_store_activity = get_all_orders().select_related().filter(pickup_date__year=year, pickup_date__month=month).values('pickup_store_id', 'pickup_store_id__name').annotate(activity=Count('pickup_store_id'))
    return_store_activity = get_all_orders().select_related().filter(return_date__year=year, return_date__month=month).values('return_store_id', 'return_store_id__name').annotate(activity=Count('return_store_id'))

    for store in stores: # For each store
        # If the current store is in the pickup_store_activity
        if (pickup_store_activity.filter(pickup_store_id=store['store_id']).count() != 0):
            # Update the pickup number for the current store
            store['pickup_activity'] = pickup_store_activity.filter(pickup_store_id=store['store_id'])[0]['activity']
        else:
            # Else, initialise it to zero
            store['pickup_activity'] = 0
        # If the current store is in the return_store_activity
        if (return_store_activity.filter(return_store_id=store['store_id']).count() != 0):
            # Update the return number for the current store
            store['return_activity'] = return_store_activity.filter(return_store_id=store['store_id'])[0]['activity']
        else:
            # Else, initialise it to zero
            store['return_activity'] = 0

        # Sum the pickup and return to get the total
        store['total_activity'] = store['pickup_activity'] + store['return_activity']

    # Create sorted versions of stores (each sorted by either their pickup, return or totals)
    pickup_store_activity = sorted(stores, key=lambda store: store['pickup_activity'], reverse=True)
    return_store_activity = sorted(stores, key=lambda store: store['return_activity'], reverse=True)
    total_store_activity = sorted(stores, key=lambda store: store['total_activity'], reverse=True)

    return {'pickup': pickup_store_activity, 'return': return_store_activity, 'total': total_store_activity}

def get_cars_per_store(year, month):
    # Get the cars that were picked up and returned to each store

    stores = get_all_stores().values('store_id') # Get a queryset of all stores

    stores_car_info = {} # To be filled with stores and car info

    for store in stores: # For each store
        # Get each car that was picked up and returned to the store (and a number of how many times they were picked up/returned)
        pickup_info = get_all_orders().select_related().filter(pickup_date__year=year, pickup_date__month=month, pickup_store_id=store['store_id']).values('car__make_name', 'car__model', 'car__seriesYear').annotate(activity=Count('car'))
        return_info = get_all_orders().select_related().filter(return_date__year=year, return_date__month=month, return_store_id=store['store_id']).values('car__make_name', 'car__model', 'car__seriesYear').annotate(activity=Count('car'))

        # Car info for the current store
        car_info = {'return': return_info, 'pickup': pickup_info}

        # For the current store, add the car info to the stores_car_info
        stores_car_info[store['store_id']] = car_info

    return stores_car_info

def get_active_customers(year, month):
    # Get the top 5 most active customers in a month

    # Get the activity of each customer and in descending order
    customer_activity = get_all_orders().select_related().filter((Q(pickup_date__year=year) & Q(pickup_date__month=month)) | (Q(return_date__year=year) & Q(return_date__month=month))).values('customer__user_id', 'customer__name').annotate(frequency=Count('customer')).order_by('-frequency')

    # Limit output to be top 5
    customer_activity = customer_activity[:5]

    return customer_activity

def generate_report(year, month):
    # Generates a report of active customers, stores and profit for a specific month

    num_prev_months = 5 # How many previous months profits to get

    # The current months profit
    month_money = [{'year': year, 'month': calendar.month_name[month], 'money': round(get_money(year, month), 2)}]

    prev_month = month
    prev_year = year

    for i in range(1, num_prev_months + 1): # For each previous month
        # Wrap the month and year if the month is January
        if (prev_month == 1):
            current_month = 12
            current_year = prev_year - 1
        else: # Decrement only the month
            current_month = prev_month - 1
            current_year = prev_year

        prev_month = current_month
        prev_year = current_year

        # Append the current, previous month to the front of the dictionary
        month_money = [{'year': current_year, 'month': calendar.month_name[current_month], 'money': round(get_money(current_year, current_month), 4)}] + month_money

    store_activity = get_store_activity(year, month)

    store_car_info = get_cars_per_store(year, month)

    active_customers = get_active_customers(year, month)

    # Calculate the difference in money from the last and second last items
    profit = round(month_money[-1]['money'] - month_money[-2]['money'], 4)

    # Whether the profit was positive or not
    if (profit >= 0):
        sign = '+'
    else:
        sign = ''

    return {'profit_history': month_money, 'profit': profit, 'sign': sign, 'store_car_info': store_car_info, 'active_customers': active_customers,
            'pickup_store': store_activity['pickup'], 'return_store': store_activity['return'], 'total_store': store_activity['total']}

def get_most_active_stores():

    # Get all the stores and have room for the pickup, return and total counters
    stores = get_all_stores().values('store_id', 'name').annotate(pickup_activity=Count('store_id'), return_activity=Count('store_id'), total_activity=Count('store_id')) # Get a queryset of all stores

    # Get a queryset of each stores (pickup counts and returns)
    pickup_store_activity = get_all_orders().select_related().values('pickup_store_id', 'pickup_store_id__name').annotate(activity=Count('pickup_store_id'))
    return_store_activity = get_all_orders().select_related().values('return_store_id', 'return_store_id__name').annotate(activity=Count('return_store_id'))

    for store in stores: # For each store
        # If the current store is in the pickup_store_activity
        if (pickup_store_activity.filter(pickup_store_id=store['store_id']).count() != 0):
            # Update the pickup number for the current store
            store['pickup_activity'] = pickup_store_activity.filter(pickup_store_id=store['store_id'])[0]['activity']
        else:
            # Else, initialise it to zero
            store['pickup_activity'] = 0
        # If the current store is in the return_store_activity
        if (return_store_activity.filter(return_store_id=store['store_id']).count() != 0):
            # Update the return number for the current store
            store['return_activity'] = return_store_activity.filter(return_store_id=store['store_id'])[0]['activity']
        else:
            # Else, initialise it to zero
            store['return_activity'] = 0

        # Sum the pickup and return to get the total
        store['total_activity'] = store['pickup_activity'] + store['return_activity']

    total_store_activity = sorted(stores, key=lambda store: store['total_activity'], reverse=True)[:10]

    return total_store_activity
