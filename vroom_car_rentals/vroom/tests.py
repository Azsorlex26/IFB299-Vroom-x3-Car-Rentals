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
