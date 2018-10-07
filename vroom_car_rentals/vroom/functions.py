from .models import *
from django.db.models import Max

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