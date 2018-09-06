from django.db import models

class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class Car(models.Model):
    car_id = models.AutoField(primary_key=True)
    make_name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    series = models.CharField(max_length=100)
    seriesYear = models.IntegerField()
    price_new = models.IntegerField()
    engine_size = models.CharField(max_length=100)
    fuel_system = models.CharField(max_length=100)
    tank_capacity = models.CharField(max_length=100)
    power = models.CharField(max_length=100)
    seating_capacity = models.IntegerField()
    standard_transmission = models.CharField(max_length=100)
    body_type = models.CharField(max_length=100)
    drive = models.CharField(max_length=100)
    wheelbase = models.CharField(max_length=100)

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    birthday = models.DateField()
    occupation = models.CharField(max_length=10)
    gender = models.CharField(max_length=1)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    password = models.CharField(max_length=100)
    salt = models.CharField(max_length=100)

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    create_date = models.DateField()
    pickup_date = models.DateField()
    pickup_store = models.ForeignKey(Store, related_name='pickup_store', on_delete=models.CASCADE)
    return_date = models.DateField()
    return_store = models.ForeignKey(Store, related_name='return_store', on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
