from django.test import TestCase
from .models import *
import datetime
from .functions import *

class GetAllCarsTests(TestCase):
    user_role = Role(role_id=1, name='Customer')

    user = User(user_id=1, name='User 1', role=user_role, password='123456', salt='123')

    store = Store(1, 'Store 1', 'address', 'phone', 'city', 'state')

    car1 = Car(1, 'make', 'model', 'series', 2003, 100, 'engine', 'fuel', 'tank', 'power', 2, 'transmission', 'body', 'wheel')
    car2 = Car(2, 'im car 2', 'model', 'series', 2003, 100, 'engine', 'fuel', 'tank', 'power', 2, 'transmission', 'body', 'wheel')
    car3 = Car(3, 'third car', 'model', 'series', 2003, 100, 'engine', 'fuel', 'tank', 'power', 2, 'transmission', 'body', 'wheel')

    def setup(self):
        # Save all the entries into the testing database
        self.user_role.save()
        self.user.save()
        self.store.save()
        self.car1.save()
        self.car2.save()
        self.car3.save()

    def test_same_cars_with_same_date(self):
        """
            If 2 copies of the same car have the same return date, the most recent one should be returned
        """
        self.setup() # Populate test table with data

        # Create two orders, that have the same return dates and same cars (other column values aren't important)
        order1 = Order(1, datetime.date(year=2018, month=4, day=22), datetime.date(year=2018, month=4, day=22), self.store.store_id, datetime.date(year=2018, month=4, day=22), self.store.store_id, self.user.user_id, self.car1.car_id)
        order2 = Order(2, datetime.date(year=2018, month=4, day=22), datetime.date(year=2018, month=4, day=22), self.store.store_id, datetime.date(year=2018, month=4, day=22), self.store.store_id, self.user.user_id, self.car1.car_id)

        # Save values into database
        order1.save()
        order2.save()

        # Should only expect the first order
        expected = Order.objects.all().filter(order_id=1)

        # Test the output is expected
        self.assertEqual(get_all_cars().__str__(), expected.__str__())

    def test_same_cars_with_different_dates(self):
        """
            If 2 copies of the same car have the different return dates, the most recent one should be returned
        """
        self.setup() # Populate test table with data

        # Create two orders, that have the same return dates and same cars (other column values aren't important)
        order1 = Order(1, datetime.date(year=2018, month=4, day=22), datetime.date(year=2018, month=4, day=22), self.store.store_id, datetime.date(year=2017, month=4, day=22), self.store.store_id, self.user.user_id, self.car1.car_id)
        order2 = Order(2, datetime.date(year=2018, month=4, day=22), datetime.date(year=2018, month=4, day=22), self.store.store_id, datetime.date(year=2018, month=4, day=22), self.store.store_id, self.user.user_id, self.car1.car_id)

        # Save values into database
        order1.save()
        order2.save()

        # Should only expect the second order
        expected = Order.objects.all().filter(order_id=2)

        # Test the output is expected
        self.assertEqual(get_all_cars().__str__(), expected.__str__())

    def test_different_cars_with_same_dates(self):
        """
            If two different cars have the same date they should both be returned
        """
        self.setup() # Populate test table with data

        # Create two orders, that have the same return dates and different cars (other column values aren't important)
        order1 = Order(1, datetime.date(year=2018, month=4, day=22), datetime.date(year=2018, month=4, day=22), self.store.store_id, datetime.date(year=2018, month=4, day=22), self.store.store_id, self.user.user_id, self.car1.car_id)
        order2 = Order(2, datetime.date(year=2018, month=4, day=22), datetime.date(year=2018, month=4, day=22), self.store.store_id, datetime.date(year=2018, month=4, day=22), self.store.store_id, self.user.user_id, self.car2.car_id)

        # Save values into database
        order1.save()
        order2.save()

        # Should exptect all orders
        expected = Order.objects.all()

        # Test the output is expected
        self.assertEqual(get_all_cars().__str__(), expected.__str__())

    def test_different_cars_with_different_dates(self):
        """
            If two different cars have different dates then they should both be returned
        """
        self.setup() # Populate test table with data

        # Create two orders, that have the different return dates and cars (other column values aren't important)
        order1 = Order(1, datetime.date(year=2018, month=4, day=22), datetime.date(year=2018, month=4, day=22), self.store.store_id, datetime.date(year=2018, month=4, day=22), self.store.store_id, self.user.user_id, self.car1.car_id)
        order2 = Order(2, datetime.date(year=2018, month=4, day=22), datetime.date(year=2018, month=4, day=22), self.store.store_id, datetime.date(year=2017, month=5, day=22), self.store.store_id, self.user.user_id, self.car2.car_id)

        # Save values into database
        order1.save()
        order2.save()

        # Should expect all orders
        expected = Order.objects.all()

        # Test the output is expected
        self.assertEqual(get_all_cars().__str__(), expected.__str__())

    def test_three_cars_same_dates_only_two_cars_same(self):
        """
            If three cars have the same date and only two are the same, then only two cars should be output
        """
        self.setup() # Populate test table with data

        # Create three orders, all cars have the same return dates but only two cars are the same (other column values aren't important)
        order1 = Order(1, datetime.date(year=2018, month=4, day=22), datetime.date(year=2018, month=4, day=22), self.store.store_id, datetime.date(year=2018, month=4, day=22), self.store.store_id, self.user.user_id, self.car1.car_id)
        order2 = Order(2, datetime.date(year=2018, month=4, day=22), datetime.date(year=2018, month=4, day=22), self.store.store_id, datetime.date(year=2018, month=4, day=22), self.store.store_id, self.user.user_id, self.car1.car_id)
        order3 = Order(3, datetime.date(year=2018, month=4, day=22), datetime.date(year=2018, month=4, day=22), self.store.store_id, datetime.date(year=2018, month=4, day=22), self.store.store_id, self.user.user_id, self.car2.car_id)

        # Save values into database
        order1.save()
        order2.save()
        order3.save()

        # Should expect orders 1 and 3
        expected = Order.objects.all().filter(order_id__in=(1, 3))

        # Test the output is expected
        self.assertEqual(get_all_cars().__str__(), expected.__str__())

    def test_three_cars_different_dates_two_cars_same(self):
        """
            If three cars have different dates and only two are the same car, then only two cars should be output
        """
        self.setup() # Populate test table with data

        # Create three orders, all cars have the different return dates but only two cars are the same (other column values aren't important)
        order1 = Order(1, datetime.date(year=2018, month=4, day=22), datetime.date(year=2018, month=4, day=22), self.store.store_id, datetime.date(year=2016, month=4, day=22), self.store.store_id, self.user.user_id, self.car1.car_id)
        order2 = Order(2, datetime.date(year=2018, month=4, day=22), datetime.date(year=2018, month=4, day=22), self.store.store_id, datetime.date(year=2017, month=4, day=22), self.store.store_id, self.user.user_id, self.car2.car_id)
        order3 = Order(3, datetime.date(year=2018, month=4, day=22), datetime.date(year=2018, month=4, day=22), self.store.store_id, datetime.date(year=2018, month=4, day=22), self.store.store_id, self.user.user_id, self.car1.car_id)

        # Save values into database
        order1.save()
        order2.save()
        order3.save()

        # Should expect orders 2 and 3
        expected = Order.objects.all().filter(order_id__in=(2, 3)) # Expect only orders 2 and 3 to be output

        # Test the output is expected
        self.assertEqual(get_all_cars().__str__(), expected.__str__())

class GenerateReportTests(TestCase):
    REVENUE_RATE = 0.2

    user_role = Role(role_id=1, name='Customer')

    user1 = User(user_id=1, name='Bob', role=user_role, password='123456', salt='123')
    user2 = User(user_id=2, name='Bobert', role=user_role, password='abcd', salt='456')
    user3 = User(user_id=3, name='Bobina', role=user_role, password='09876', salt='789')
    user4 = User(user_id=4, name='Bobette', role=user_role, password='zyxwv', salt='101112')
    user5 = User(user_id=5, name='Bobbo', role=user_role, password='qwerty', salt='131415')
    user6 = User(user_id=6, name='Bobob', role=user_role, password='password', salt='161718')
    user7 = User(user_id=7, name='Bobe', role=user_role, password='0000', salt='192021')

    store1 = Store(1, 'Store 1', 'address', 'phone', 'city', 'state')
    store2 = Store(2, 'Store 2', 'address2', 'phone2', 'city2', 'state2')
    store3 = Store(3, 'Store 3', 'address3', 'phone3', 'city3', 'state3')
    store4 = Store(4, 'Store 4', 'address4', 'phone4', 'city4', 'state4')
    store5 = Store(5, 'Store 5', 'address5', 'phone5', 'city5', 'state5')
    store6 = Store(6, 'Store 6', 'address6', 'phone6', 'city6', 'state6')
    store7 = Store(7, 'Store 7', 'address7', 'phone7', 'city7', 'state7')


    car1 = Car(1, 'make', 'model', 'series', 2003, 51444, 'engine', 'fuel', 'tank', 'power', 2, 'transmission', 'body', 'wheel')
    car2 = Car(2, 'im car 2', 'model', 'series', 2003, 85621, 'engine', 'fuel', 'tank', 'power', 2, 'transmission', 'body', 'wheel')
    car3 = Car(3, 'third car', 'model', 'series', 2003, 20588, 'engine', 'fuel', 'tank', 'power', 2, 'transmission', 'body', 'wheel')
    car4 = Car(4, 'forf car', 'model', 'series', 2003, 70348, 'engine', 'fuel', 'tank', 'power', 2, 'transmission', 'body', 'wheel')
    car5 = Car(5, 'fif car', 'model', 'series', 2003, 51796, 'engine', 'fuel', 'tank', 'power', 2, 'transmission', 'body', 'wheel')
    car6 = Car(6, 'car sicks', 'model', 'series', 2003, 97296, 'engine', 'fuel', 'tank', 'power', 2, 'transmission', 'body', 'wheel')
    car7 = Car(7, "Car 7'); DROP TABLE vroom_car;--", 'model', 'series', 2003, 11940, 'engine', 'fuel', 'tank', 'power', 2, 'transmission', 'body', 'wheel')

    def setup(self):
        # Save all the entries into the testing database
        self.user_role.save()
        self.user1.save()
        self.user2.save()
        self.user3.save()
        self.user4.save()
        self.user5.save()
        self.user6.save()
        self.user7.save()
        self.store1.save()
        self.store2.save()
        self.store3.save()
        self.store4.save()
        self.store5.save()
        self.store6.save()
        self.store7.save()
        self.car1.save()
        self.car2.save()
        self.car3.save()
        self.car4.save()
        self.car5.save()
        self.car6.save()
        self.car7.save()

    def test_min_order_date_same_date(self):
        """
            If there are two orders with the lowest date, it shouldn't matter which is selected, but should expect an output
        """
        self.setup() # Populate test table with data

        # Create two orders, both have the same creation date
        order1 = Order(1, datetime.date(year=2018, month=4, day=22), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2016, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car1.car_id)
        order2 = Order(2, datetime.date(year=2018, month=4, day=22), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2017, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car2.car_id)

        # Save values into database
        order1.save()
        order2.save()

        # Should expect order 1
        expected = Order.objects.all().filter(order_id=1) # Expect only the first order

        # Test the output is expected
        self.assertEqual(get_min_order_date()['min_date'].__str__(), expected[0].create_date.__str__())

    def test_min_order_date_middle(self):
        """
            If there are three orders and the one in the middle is the earliest, it should be returned
        """
        self.setup() # Populate test table with data

        # Create three orders, the middle order is the earliest created
        order1 = Order(1, datetime.date(year=2018, month=4, day=29), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2016, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car1.car_id)
        order2 = Order(2, datetime.date(year=2017, month=4, day=7), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2017, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car2.car_id)
        order3 = Order(3, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2017, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car2.car_id)

        # Save values into database
        order1.save()
        order2.save()
        order3.save()

        # Should expect second order
        expected = Order.objects.all().filter(order_id=2) # Expect only the second order

        # Test the output is expected
        self.assertEqual(get_min_order_date()['min_date'].__str__(), expected[0].create_date.__str__())

    def test_min_order_date_not_oldest(self):
        """
            If one of the return dates is earlier than another orders creation date (shouldn't ever be), the oldest creation date should be retrieved
        """

        self.setup() # Populate test table with data

        # Create two orders, first has newest create date but has a return date older than the oldest create date
        order1 = Order(1, datetime.date(year=2018, month=4, day=29), datetime.date(year=2005, month=4, day=22), self.store1.store_id, datetime.date(year=2005, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car1.car_id)
        order2 = Order(2, datetime.date(year=2017, month=4, day=7), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2017, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car2.car_id)

        # Save values into database
        order1.save()
        order2.save()

        # Should expect second order
        expected = Order.objects.all().filter(order_id=2) # Expect only the second order

        # Test the output is expected
        self.assertEqual(get_min_order_date()['min_date'].__str__(), expected[0].create_date.__str__())

    def test_max_order_date_same_date(self):
        """
            If there are two orders with the highest return date, it shouldn't matter which is selected, but should expect an output (the first one in the database)
        """
        self.setup() # Populate test table with data

        # Create two orders, both have the same creation date
        order1 = Order(1, datetime.date(year=2018, month=4, day=19), datetime.date(year=2004, month=9, day=15), self.store1.store_id, datetime.date(year=2016, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car1.car_id)
        order2 = Order(2, datetime.date(year=2014, month=7, day=22), datetime.date(year=2008, month=5, day=1), self.store1.store_id, datetime.date(year=2016, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car2.car_id)

        # Save values into database
        order1.save()
        order2.save()

        # Should expect order 1
        expected = Order.objects.all().filter(order_id=1) # Expect only the first order

        # Test the output is expected
        self.assertEqual(get_max_order_date()['max_date'].__str__(), expected[0].return_date.__str__())

    def test_max_order_date_middle(self):
        """
            If there are three orders and the one in the middle is the most recent, it should be returned
        """
        self.setup() # Populate test table with data

        # Create three orders, the middle order is the most recently returned
        order1 = Order(1, datetime.date(year=2018, month=4, day=29), datetime.date(year=2018, month=1, day=15), self.store1.store_id, datetime.date(year=2005, month=4, day=20), self.store1.store_id, self.user1.user_id, self.car1.car_id)
        order2 = Order(2, datetime.date(year=2017, month=4, day=7), datetime.date(year=2002, month=4, day=22), self.store1.store_id, datetime.date(year=2017, month=10, day=2), self.store1.store_id, self.user1.user_id, self.car2.car_id)
        order3 = Order(3, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=9, day=8), self.store1.store_id, datetime.date(year=2004, month=12, day=30), self.store1.store_id, self.user1.user_id, self.car2.car_id)

        # Save values into database
        order1.save()
        order2.save()
        order3.save()

        # Should expect second order
        expected = Order.objects.all().filter(order_id=2) # Expect only the second order

        # Test the output is expected
        self.assertEqual(get_max_order_date()['max_date'].__str__(), expected[0].return_date.__str__())

    def test_max_order_date_not_oldest(self):
        """
            If one of the create dates is earlier than another orders return date (shouldn't ever be), the oldest return date should be retrieved
        """

        self.setup() # Populate test table with data

        # Create two orders, first has newest create date but has a return date older than the newest return date
        order1 = Order(1, datetime.date(year=2018, month=4, day=29), datetime.date(year=2005, month=4, day=22), self.store1.store_id, datetime.date(year=2005, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car1.car_id)
        order2 = Order(2, datetime.date(year=2017, month=4, day=7), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2017, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car2.car_id)

        # Save values into database
        order1.save()
        order2.save()

        # Should expect second order
        expected = Order.objects.all().filter(order_id=2) # Expect only the second order

        # Test the output is expected
        self.assertEqual(get_max_order_date()['max_date'].__str__(), expected[0].return_date.__str__())

    def test_get_money_same_month(self):
        """
            If all orders are for the same pickup month, the sum of each cars price should be returned
        """
        self.setup() # Populate test table with data

        # Create six orders, all with the same pickup month, using cars 1, 2, 2, 7, 4, 3
        order1 = Order(1, datetime.date(year=2018, month=4, day=29), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2016, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car1.car_id)
        order2 = Order(2, datetime.date(year=2017, month=4, day=7), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2017, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car2.car_id)
        order3 = Order(3, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2017, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car2.car_id)
        order4 = Order(4, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2017, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car7.car_id)
        order5 = Order(5, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2017, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car4.car_id)
        order6 = Order(6, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2017, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car3.car_id)

        # Save values into database
        order1.save()
        order2.save()
        order3.save()
        order4.save()
        order5.save()
        order6.save()

        # Should expect the sum of each orders car
        expected = self.REVENUE_RATE * (order1.car.price_new + order2.car.price_new + order3.car.price_new + order4.car.price_new + order5.car.price_new + order6.car.price_new)

        # Test the output is expected
        self.assertEqual(get_money(2018, 4), expected)

    def test_get_money_different_months(self):
        """
            If some orders are from a different pickup month, they shouldn't be added to the total
        """
        self.setup() # Populate test table with data

        # Create eight orders, six have the same pickup month (using cars 1, 2, 2, 7, 4, 3), the other two are from another month
        order1 = Order(1, datetime.date(year=2018, month=4, day=29), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2016, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car1.car_id)
        order2 = Order(2, datetime.date(year=2017, month=4, day=7), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2017, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car2.car_id)
        order3 = Order(3, datetime.date(year=2017, month=4, day=7), datetime.date(year=2016, month=4, day=22), self.store1.store_id, datetime.date(year=2016, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car5.car_id)
        order4 = Order(4, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2017, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car2.car_id)
        order5 = Order(5, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2017, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car7.car_id)
        order6 = Order(6, datetime.date(year=2018, month=1, day=16), datetime.date(year=2016, month=4, day=22), self.store1.store_id, datetime.date(year=2016, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car6.car_id)
        order7 = Order(7, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2017, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car4.car_id)
        order8 = Order(8, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2017, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car3.car_id)

        # Save values into database
        order1.save()
        order2.save()
        order3.save()
        order4.save()
        order5.save()
        order6.save()
        order7.save()
        order8.save()

        # Should expect the sum of orders 1, 2, 4, 5, 7 and 8
        expected = self.REVENUE_RATE * (order1.car.price_new + order2.car.price_new + order4.car.price_new + order5.car.price_new + order7.car.price_new + order8.car.price_new)

        # Test the output is expected
        self.assertEqual(get_money(2018, 4), expected)

    def test_get_money_empty_month(self):
        """
            If there are no orders for the specified month, 0 should be returned
        """
        self.setup() # Populate test table with data

        # Create eight orders, six have the same pickup month (using cars 1, 2, 2, 7, 4, 3), the other two are from another month
        order1 = Order(1, datetime.date(year=2018, month=4, day=29), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2016, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car1.car_id)
        order2 = Order(2, datetime.date(year=2017, month=4, day=7), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2017, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car2.car_id)
        order3 = Order(3, datetime.date(year=2017, month=4, day=7), datetime.date(year=2016, month=4, day=22), self.store1.store_id, datetime.date(year=2016, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car5.car_id)
        order4 = Order(4, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2017, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car2.car_id)
        order5 = Order(5, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2017, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car7.car_id)
        order6 = Order(6, datetime.date(year=2018, month=1, day=16), datetime.date(year=2016, month=4, day=22), self.store1.store_id, datetime.date(year=2016, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car6.car_id)
        order7 = Order(7, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2017, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car4.car_id)
        order8 = Order(8, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2017, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car3.car_id)

        # Save values into database
        order1.save()
        order2.save()
        order3.save()
        order4.save()
        order5.save()
        order6.save()
        order7.save()
        order8.save()

        # Should expect 0
        expected = 0

        # Test the output is expected
        self.assertEqual(get_money(2014, 2), expected)

    def test_get_store_activity_total_activity(self):
        """
            If all stores have activity, the total stores returned should be ordered by their total acitvity
        """
        self.setup() # Populate test table with data

        # Create ten orders with activity of each store:
        #       Store 1: P: 1, R: 2, T: 3
        #       Store 2: P: 2, R: 3, T: 5
        #       Store 3: P: 3, R: 1, T: 4
        #       Store 4: P: 0, R: 2, T: 2
        #       Store 5: P: 2, R: 1, T: 3
        #       Store 6: P: 1, R: 1, T: 2
        #       Store 7: P: 1, R: 0, T: 1
        order1 = Order(1, datetime.date(year=2018, month=4, day=29), datetime.date(year=2018, month=4, day=22), self.store5.store_id, datetime.date(year=2018, month=4, day=22), self.store2.store_id, self.user1.user_id, self.car1.car_id)
        order2 = Order(2, datetime.date(year=2017, month=4, day=7), datetime.date(year=2018, month=4, day=22), self.store5.store_id, datetime.date(year=2018, month=4, day=22), self.store6.store_id, self.user1.user_id, self.car2.car_id)
        order3 = Order(3, datetime.date(year=2017, month=4, day=7), datetime.date(year=2018, month=4, day=22), self.store3.store_id, datetime.date(year=2018, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car5.car_id)
        order4 = Order(4, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store3.store_id, datetime.date(year=2018, month=4, day=22), self.store3.store_id, self.user1.user_id, self.car2.car_id)
        order5 = Order(5, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store6.store_id, datetime.date(year=2018, month=4, day=22), self.store2.store_id, self.user1.user_id, self.car7.car_id)
        order6 = Order(6, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2018, month=4, day=22), self.store4.store_id, self.user1.user_id, self.car6.car_id)
        order7 = Order(7, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store2.store_id, datetime.date(year=2018, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car4.car_id)
        order8 = Order(8, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store7.store_id, datetime.date(year=2018, month=4, day=22), self.store5.store_id, self.user1.user_id, self.car3.car_id)
        order9 = Order(9, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store3.store_id, datetime.date(year=2018, month=4, day=22), self.store2.store_id, self.user1.user_id, self.car3.car_id)
        order10 = Order(10, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store2.store_id, datetime.date(year=2018, month=4, day=22), self.store4.store_id, self.user1.user_id, self.car3.car_id)

        # Save values into database
        order1.save()
        order2.save()
        order3.save()
        order4.save()
        order5.save()
        order6.save()
        order7.save()
        order8.save()
        order9.save()
        order10.save()

        # Should output of stores and their total orders (in descending order)
        expected = [[self.store2.store_id, 5],
                    [self.store3.store_id, 4],
                    [self.store1.store_id, 3],
                    [self.store5.store_id, 3],
                    [self.store4.store_id, 2],
                    [self.store6.store_id, 2],
                    [self.store7.store_id, 1]]

        stores = get_store_activity(2018, 4)

        calculated = [] # Creating an array of the same format as expected
        for store in stores['total']:
            calculated.append([store['store_id'], store['total_activity']])

        # Test the output is expected
        self.assertEqual(calculated.__str__(), expected.__str__())

    def test_get_store_activity_pickup_activity(self):
        """
            If all stores have activity, the total stores returned should be ordered by their pickup acitvity
        """
        self.setup() # Populate test table with data

        # Create ten orders with activity of each store:
        #       Store 1: P: 1, R: 2, T: 3
        #       Store 2: P: 2, R: 3, T: 5
        #       Store 3: P: 3, R: 1, T: 4
        #       Store 4: P: 0, R: 2, T: 2
        #       Store 5: P: 2, R: 1, T: 3
        #       Store 6: P: 1, R: 1, T: 2
        #       Store 7: P: 1, R: 0, T: 1
        order1 = Order(1, datetime.date(year=2018, month=4, day=29), datetime.date(year=2018, month=4, day=22), self.store5.store_id, datetime.date(year=2018, month=4, day=22), self.store2.store_id, self.user1.user_id, self.car1.car_id)
        order2 = Order(2, datetime.date(year=2017, month=4, day=7), datetime.date(year=2018, month=4, day=22), self.store5.store_id, datetime.date(year=2018, month=4, day=22), self.store6.store_id, self.user1.user_id, self.car2.car_id)
        order3 = Order(3, datetime.date(year=2017, month=4, day=7), datetime.date(year=2018, month=4, day=22), self.store3.store_id, datetime.date(year=2018, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car5.car_id)
        order4 = Order(4, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store3.store_id, datetime.date(year=2018, month=4, day=22), self.store3.store_id, self.user1.user_id, self.car2.car_id)
        order5 = Order(5, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store6.store_id, datetime.date(year=2018, month=4, day=22), self.store2.store_id, self.user1.user_id, self.car7.car_id)
        order6 = Order(6, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2018, month=4, day=22), self.store4.store_id, self.user1.user_id, self.car6.car_id)
        order7 = Order(7, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store2.store_id, datetime.date(year=2018, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car4.car_id)
        order8 = Order(8, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store7.store_id, datetime.date(year=2018, month=4, day=22), self.store5.store_id, self.user1.user_id, self.car3.car_id)
        order9 = Order(9, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store3.store_id, datetime.date(year=2018, month=4, day=22), self.store2.store_id, self.user1.user_id, self.car3.car_id)
        order10 = Order(10, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store2.store_id, datetime.date(year=2018, month=4, day=22), self.store4.store_id, self.user1.user_id, self.car3.car_id)

        # Save values into database
        order1.save()
        order2.save()
        order3.save()
        order4.save()
        order5.save()
        order6.save()
        order7.save()
        order8.save()
        order9.save()
        order10.save()

        # Should output of stores and their pickup orders (in descending order)
        expected = [[self.store3.store_id, 3],
                    [self.store2.store_id, 2],
                    [self.store5.store_id, 2],
                    [self.store1.store_id, 1],
                    [self.store6.store_id, 1],
                    [self.store7.store_id, 1],
                    [self.store4.store_id, 0]]

        stores = get_store_activity(2018, 4)

        calculated = [] # Creating an array of the same format as expected
        for store in stores['pickup']:
            calculated.append([store['store_id'], store['pickup_activity']])

        # Test the output is expected
        self.assertEqual(calculated.__str__(), expected.__str__())

    def test_get_store_activity_return_activity(self):
        """
            If all stores have activity, the total stores returned should be ordered by their return acitvity
        """
        self.setup() # Populate test table with data

        # Create ten orders with activity of each store:
        #       Store 1: P: 1, R: 2, T: 3
        #       Store 2: P: 2, R: 3, T: 5
        #       Store 3: P: 3, R: 1, T: 4
        #       Store 4: P: 0, R: 2, T: 2
        #       Store 5: P: 2, R: 1, T: 3
        #       Store 6: P: 1, R: 1, T: 2
        #       Store 7: P: 1, R: 0, T: 1
        order1 = Order(1, datetime.date(year=2018, month=4, day=29), datetime.date(year=2018, month=4, day=22), self.store5.store_id, datetime.date(year=2018, month=4, day=22), self.store2.store_id, self.user1.user_id, self.car1.car_id)
        order2 = Order(2, datetime.date(year=2017, month=4, day=7), datetime.date(year=2018, month=4, day=22), self.store5.store_id, datetime.date(year=2018, month=4, day=22), self.store6.store_id, self.user1.user_id, self.car2.car_id)
        order3 = Order(3, datetime.date(year=2017, month=4, day=7), datetime.date(year=2018, month=4, day=22), self.store3.store_id, datetime.date(year=2018, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car5.car_id)
        order4 = Order(4, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store3.store_id, datetime.date(year=2018, month=4, day=22), self.store3.store_id, self.user1.user_id, self.car2.car_id)
        order5 = Order(5, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store6.store_id, datetime.date(year=2018, month=4, day=22), self.store2.store_id, self.user1.user_id, self.car7.car_id)
        order6 = Order(6, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2018, month=4, day=22), self.store4.store_id, self.user1.user_id, self.car6.car_id)
        order7 = Order(7, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store2.store_id, datetime.date(year=2018, month=4, day=22), self.store1.store_id, self.user1.user_id, self.car4.car_id)
        order8 = Order(8, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store7.store_id, datetime.date(year=2018, month=4, day=22), self.store5.store_id, self.user1.user_id, self.car3.car_id)
        order9 = Order(9, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store3.store_id, datetime.date(year=2018, month=4, day=22), self.store2.store_id, self.user1.user_id, self.car3.car_id)
        order10 = Order(10, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store2.store_id, datetime.date(year=2018, month=4, day=22), self.store4.store_id, self.user1.user_id, self.car3.car_id)

        # Save values into database
        order1.save()
        order2.save()
        order3.save()
        order4.save()
        order5.save()
        order6.save()
        order7.save()
        order8.save()
        order9.save()
        order10.save()

        # Should output of stores and their return orders (in descending order)
        expected = [[self.store2.store_id, 3],
                    [self.store1.store_id, 2],
                    [self.store4.store_id, 2],
                    [self.store3.store_id, 1],
                    [self.store5.store_id, 1],
                    [self.store6.store_id, 1],
                    [self.store7.store_id, 0]]

        stores = get_store_activity(2018, 4)

        calculated = [] # Creating an array of the same format as expected
        for store in stores['return']:
            calculated.append([store['store_id'], store['return_activity']])

        # Test the output is expected
        self.assertEqual(calculated.__str__(), expected.__str__())

    def test_get_active_customers(self):
        """
            If customers all have different activites, they should be returned in descending order (by how many orders they had)
        """
        self.setup() # Populate test table with data

        # Create eleven orders with activity of each store:
        #       Customer 1: 0
        #       Customer 2: 3
        #       Customer 3: 2
        #       Customer 4: 4
        #       Customer 5: 0
        #       Customer 6: 1
        #       Customer 7: 1
        order1 = Order(1, datetime.date(year=2018, month=4, day=29), datetime.date(year=2018, month=4, day=22), self.store5.store_id, datetime.date(year=2018, month=4, day=22), self.store2.store_id, self.user3.user_id, self.car1.car_id)
        order2 = Order(2, datetime.date(year=2017, month=4, day=7), datetime.date(year=2018, month=4, day=22), self.store5.store_id, datetime.date(year=2018, month=4, day=22), self.store6.store_id, self.user2.user_id, self.car2.car_id)
        order3 = Order(3, datetime.date(year=2017, month=4, day=7), datetime.date(year=2018, month=4, day=22), self.store3.store_id, datetime.date(year=2018, month=4, day=22), self.store1.store_id, self.user4.user_id, self.car5.car_id)
        order4 = Order(4, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store3.store_id, datetime.date(year=2018, month=4, day=22), self.store3.store_id, self.user6.user_id, self.car2.car_id)
        order5 = Order(5, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store6.store_id, datetime.date(year=2018, month=4, day=22), self.store2.store_id, self.user3.user_id, self.car7.car_id)
        order6 = Order(6, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2018, month=4, day=22), self.store4.store_id, self.user2.user_id, self.car6.car_id)
        order7 = Order(7, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store2.store_id, datetime.date(year=2018, month=4, day=22), self.store1.store_id, self.user4.user_id, self.car4.car_id)
        order8 = Order(8, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store7.store_id, datetime.date(year=2018, month=4, day=22), self.store5.store_id, self.user2.user_id, self.car3.car_id)
        order9 = Order(9, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store3.store_id, datetime.date(year=2018, month=4, day=22), self.store2.store_id, self.user7.user_id, self.car3.car_id)
        order10 = Order(10, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store2.store_id, datetime.date(year=2018, month=4, day=22), self.store4.store_id, self.user4.user_id, self.car3.car_id)
        order11 = Order(11, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store2.store_id, datetime.date(year=2018, month=4, day=22), self.store4.store_id, self.user4.user_id, self.car3.car_id)

        # Save values into database
        order1.save()
        order2.save()
        order3.save()
        order4.save()
        order5.save()
        order6.save()
        order7.save()
        order8.save()
        order9.save()
        order10.save()
        order11.save()

        # Should output the top 5 active customers and the number of orders they were in (in descending order)
        expected = [[self.user4.user_id, 4],
                    [self.user2.user_id, 3],
                    [self.user3.user_id, 2],
                    [self.user6.user_id, 1],
                    [self.user7.user_id, 1]]

        customers = get_active_customers(2018, 4)

        calculated = [] # Creating an array of the same format as expected
        for customer in customers:
            calculated.append([customer['customer__user_id'], customer['frequency']])

        # Test the output is expected
        self.assertEqual(calculated.__str__(), expected.__str__())

    def test_get_active_customers_other_customer_month(self):
        """
            If a customer has a high activity in a different month, it shouldn't be considered
        """
        self.setup() # Populate test table with data

        # Create eleven orders with activity of each store:
        #       Customer 1: 5 (in other months)
        #       Customer 2: 3
        #       Customer 3: 2
        #       Customer 4: 4
        #       Customer 5: 0
        #       Customer 6: 1
        #       Customer 7: 1
        order1 = Order(1, datetime.date(year=2018, month=4, day=29), datetime.date(year=2018, month=4, day=22), self.store5.store_id, datetime.date(year=2018, month=4, day=22), self.store2.store_id, self.user3.user_id, self.car1.car_id)
        order2 = Order(2, datetime.date(year=2017, month=4, day=7), datetime.date(year=2018, month=4, day=22), self.store5.store_id, datetime.date(year=2018, month=4, day=22), self.store6.store_id, self.user2.user_id, self.car2.car_id)
        order3 = Order(3, datetime.date(year=2017, month=4, day=7), datetime.date(year=2018, month=4, day=22), self.store3.store_id, datetime.date(year=2018, month=4, day=22), self.store1.store_id, self.user4.user_id, self.car5.car_id)
        order4 = Order(4, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store3.store_id, datetime.date(year=2018, month=4, day=22), self.store3.store_id, self.user6.user_id, self.car2.car_id)
        order5 = Order(5, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store6.store_id, datetime.date(year=2018, month=4, day=22), self.store2.store_id, self.user3.user_id, self.car7.car_id)
        order6 = Order(6, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2018, month=4, day=22), self.store4.store_id, self.user2.user_id, self.car6.car_id)
        order7 = Order(7, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store2.store_id, datetime.date(year=2018, month=4, day=22), self.store1.store_id, self.user4.user_id, self.car4.car_id)
        order8 = Order(8, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store7.store_id, datetime.date(year=2018, month=4, day=22), self.store5.store_id, self.user2.user_id, self.car3.car_id)
        order9 = Order(9, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store3.store_id, datetime.date(year=2018, month=4, day=22), self.store2.store_id, self.user7.user_id, self.car3.car_id)
        order10 = Order(10, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store2.store_id, datetime.date(year=2018, month=4, day=22), self.store4.store_id, self.user4.user_id, self.car3.car_id)
        order11 = Order(11, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store2.store_id, datetime.date(year=2018, month=4, day=22), self.store4.store_id, self.user4.user_id, self.car3.car_id)
        order12 = Order(12, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store2.store_id, datetime.date(year=2018, month=4, day=22), self.store4.store_id, self.user1.user_id, self.car3.car_id)
        order13 = Order(13, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store2.store_id, datetime.date(year=2018, month=4, day=22), self.store4.store_id, self.user1.user_id, self.car3.car_id)
        order14 = Order(14, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store2.store_id, datetime.date(year=2018, month=4, day=22), self.store4.store_id, self.user1.user_id, self.car3.car_id)
        order15 = Order(15, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store2.store_id, datetime.date(year=2018, month=4, day=22), self.store4.store_id, self.user1.user_id, self.car3.car_id)
        order16 = Order(16, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store2.store_id, datetime.date(year=2018, month=4, day=22), self.store4.store_id, self.user1.user_id, self.car3.car_id)

        # Save values into database
        order1.save()
        order2.save()
        order3.save()
        order4.save()
        order5.save()
        order6.save()
        order7.save()
        order8.save()
        order9.save()
        order10.save()
        order11.save()

        # Should output the top 5 active customers and the number of orders they were in (in descending order)
        expected = [[self.user4.user_id, 4],
                    [self.user2.user_id, 3],
                    [self.user3.user_id, 2],
                    [self.user6.user_id, 1],
                    [self.user7.user_id, 1]]

        customers = get_active_customers(2018, 4)

        calculated = [] # Creating an array of the same format as expected
        for customer in customers:
            calculated.append([customer['customer__user_id'], customer['frequency']])

        # Test the output is expected
        self.assertEqual(calculated.__str__(), expected.__str__())

    def test_get_active_customers_other_months(self):
        """
            If a customer has activity in other months, those months shouldn't count
        """
        self.setup() # Populate test table with data

        # Create eleven orders with activity of each store:
        #       Customer 1: 0
        #       Customer 2: 3
        #       Customer 3: 2
        #       Customer 4: 6 (2 in other months)
        #       Customer 5: 0
        #       Customer 6: 1
        #       Customer 7: 1
        order1 = Order(1, datetime.date(year=2018, month=4, day=29), datetime.date(year=2018, month=4, day=22), self.store5.store_id, datetime.date(year=2018, month=4, day=22), self.store2.store_id, self.user3.user_id, self.car1.car_id)
        order2 = Order(2, datetime.date(year=2017, month=4, day=7), datetime.date(year=2018, month=4, day=22), self.store5.store_id, datetime.date(year=2018, month=4, day=22), self.store6.store_id, self.user2.user_id, self.car2.car_id)
        order3 = Order(3, datetime.date(year=2017, month=4, day=7), datetime.date(year=2018, month=4, day=22), self.store3.store_id, datetime.date(year=2018, month=4, day=22), self.store1.store_id, self.user4.user_id, self.car5.car_id)
        order4 = Order(4, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store3.store_id, datetime.date(year=2018, month=4, day=22), self.store3.store_id, self.user6.user_id, self.car2.car_id)
        order5 = Order(5, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store6.store_id, datetime.date(year=2018, month=4, day=22), self.store2.store_id, self.user3.user_id, self.car7.car_id)
        order6 = Order(6, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store1.store_id, datetime.date(year=2018, month=4, day=22), self.store4.store_id, self.user2.user_id, self.car6.car_id)
        order7 = Order(7, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store2.store_id, datetime.date(year=2018, month=4, day=22), self.store1.store_id, self.user4.user_id, self.car4.car_id)
        order8 = Order(8, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store7.store_id, datetime.date(year=2018, month=4, day=22), self.store5.store_id, self.user2.user_id, self.car3.car_id)
        order9 = Order(9, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store3.store_id, datetime.date(year=2018, month=4, day=22), self.store2.store_id, self.user7.user_id, self.car3.car_id)
        order10 = Order(10, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store2.store_id, datetime.date(year=2018, month=4, day=22), self.store4.store_id, self.user4.user_id, self.car3.car_id)
        order11 = Order(11, datetime.date(year=2018, month=1, day=16), datetime.date(year=2018, month=4, day=22), self.store2.store_id, datetime.date(year=2018, month=4, day=22), self.store4.store_id, self.user4.user_id, self.car3.car_id)
        order12 = Order(12, datetime.date(year=2018, month=1, day=16), datetime.date(year=2016, month=4, day=22), self.store2.store_id, datetime.date(year=2016, month=4, day=22), self.store4.store_id, self.user4.user_id, self.car3.car_id)
        order13 = Order(13, datetime.date(year=2018, month=1, day=16), datetime.date(year=2016, month=4, day=22), self.store2.store_id, datetime.date(year=2016, month=4, day=22), self.store4.store_id, self.user4.user_id, self.car3.car_id)

        # Save values into database
        order1.save()
        order2.save()
        order3.save()
        order4.save()
        order5.save()
        order6.save()
        order7.save()
        order8.save()
        order9.save()
        order10.save()
        order11.save()

        # Should output the top 5 active customers and the number of orders they were in (in descending order)
        expected = [[self.user4.user_id, 4],
                    [self.user2.user_id, 3],
                    [self.user3.user_id, 2],
                    [self.user6.user_id, 1],
                    [self.user7.user_id, 1]]

        customers = get_active_customers(2018, 4)

        calculated = [] # Creating an array of the same format as expected
        for customer in customers:
            calculated.append([customer['customer__user_id'], customer['frequency']])

        # Test the output is expected
        self.assertEqual(calculated.__str__(), expected.__str__())

    def test_generate_report_months_same_year(self):
        """
            If the report is generated for a month where the previous 5 months are in the same year, the previous months calculated should be in the same year
        """

        # Expected months output (format: year, month)
        expected = [[2018, 'April'],
                    [2018, 'May'],
                    [2018, 'June'],
                    [2018, 'July'],
                    [2018, 'August'],
                    [2018, 'September']]

        report = generate_report(2018, 9)

        calculated = [] # Match format of expected
        for month in report['profit_history']:
            calculated.append([month['year'], month['month']])

        # Test the output is expected
        self.assertEqual(calculated.__str__(), expected.__str__())

    def test_generate_report_months_different_year(self):
        """
            If the report is generated for a month where the previous 5 months roll over to the previous year, the previous months calculated should change year
        """

        # Expected months output (format: year, month)
        expected = [[2017, 'September'],
                    [2017, 'October'],
                    [2017, 'November'],
                    [2017, 'December'],
                    [2018, 'January'],
                    [2018, 'February']]

        report = generate_report(2018, 2)

        calculated = [] # Match format of expected
        for month in report['profit_history']:
            calculated.append([month['year'], month['month']])

        # Test the output is expected
        self.assertEqual(calculated.__str__(), expected.__str__())
