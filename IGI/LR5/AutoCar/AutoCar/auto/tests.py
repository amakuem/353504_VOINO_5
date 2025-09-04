from django.test import TestCase, Client as TestClient  # Переименовываем встроенный Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Client, Car, ParkingPlace, Invoice, Review, CompanyInfo

class ClientModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client_obj = Client.objects.create(
            user=self.user,
            phone_number='+375 (29) 123-45-67',
            birth_date='1990-01-01'
        )

    def test_client_creation(self):
        self.assertEqual(self.client_obj.user.username, 'testuser')
        self.assertEqual(str(self.client_obj), 'testuser')

    def test_phone_validation(self):
        invalid_numbers = [
            '+375 (29) 123-4',
            '375291234567',
            'test string'
        ]
        for number in invalid_numbers:
            with self.subTest(number=number):
                client = Client(
                    user=self.user,
                    phone_number=number,
                    birth_date='2000-01-01'
                )
                self.assertRaises(ValidationError, client.full_clean)

class ParkingPlaceTest(TestCase):
    def test_unique_number(self):
        ParkingPlace.objects.create(number=1, price=100)
        with self.assertRaises(IntegrityError):
            ParkingPlace.objects.create(number=1, price=150)

class CarViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client_obj = Client.objects.create(
            user=self.user,
            phone_number='+375 (29) 123-45-67',
            birth_date='1990-01-01'
        )
        self.parking = ParkingPlace.objects.create(
            number=1, 
            price=100,
            is_occupied=False
        )
        self.car_data = {
            'license_plate': 'AB1234',
            'model': 'Tesla Model S',
            'parking_place': self.parking.id
        }
        self.test_client = TestClient()

    def test_car_creation_flow(self):
        self.test_client.login(username='testuser', password='testpass123')
        response = self.test_client.post(
            reverse('car_create'),
            data=self.car_data
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Car.objects.count(), 1)
        
        updated_parking = ParkingPlace.objects.get(id=self.parking.id)
        self.assertTrue(updated_parking.is_occupied)
        
        invoice = Invoice.objects.first()
        self.assertEqual(invoice.amount, 100)
        self.assertFalse(invoice.is_payment)

    def test_car_attach_flow(self):
        # Создаем отдельного владельца для автомобиля
        owner_user = User.objects.create_user(
            username='owner',
            password='testpass123'
        )
        owner_client = Client.objects.create(
            user=owner_user,
            phone_number='+375 (29) 765-43-21',
            birth_date='1995-01-01'
        )
        
        car = Car.objects.create(
            license_plate='BC5678',
            model='BMW X5',
            owner=owner_client,
            parking_place=self.parking
        )
        
        self.test_client.login(username='testuser', password='testpass123')
        response = self.test_client.post(
            reverse('car_attach'),
            {'license_plate': 'BC5678'},
            follow=True
        )
        
        self.assertEqual(response.status_code, 200)
        car.refresh_from_db()
        self.assertEqual(car.clients.count(), 1)
        self.assertRedirects(response, reverse('profile'))

class ViewTests(TestCase):
    def setUp(self):
        self.test_client = TestClient()  # Используем переименованный Client
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client_obj = Client.objects.create(
            user=self.user,
            phone_number='+375 (29) 123-45-67',
            birth_date='1990-01-01'
        )

    def test_home_page(self):
        response = self.test_client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Calendar', status_code=200)

    def test_protected_views(self):
        response = self.test_client.get(reverse('profile'))
        self.assertRedirects(
            response, 
            '/accounts/login/?next=/profile/',
            status_code=302,
            target_status_code=404
        )

    def test_registration(self):
        response = self.test_client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'email': 'new@example.com',
            'phone_number': '+375 (29) 765-43-21',
            'birth_date': '2000-01-01'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 2)

class AdminViewsTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass'
        )
        self.test_client = TestClient()
        self.test_client.force_login(self.admin)

    def test_parking_list_view(self):
        parking = ParkingPlace.objects.create(number=1, price=100)
        response = self.test_client.get(reverse('parking_list'))
        
        # Проверяем отображение номера в таблице
        self.assertContains(
            response, 
            f'<td>{parking.number}</td>',
            html=True
        )
        
        # Проверяем обновление цены
        new_price = 150
        response = self.test_client.post(
            reverse('parking_list'),
            {'place_id': parking.id, 'price': new_price}
        )
        parking.refresh_from_db()
        self.assertEqual(parking.price, new_price)