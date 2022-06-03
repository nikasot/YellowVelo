from django.test import TestCase
from django.test.client import Client
from shop.models import User, Cycle, Category


# Create your tests here.
class ModelTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()

    # Проверка доступности домашней страницы
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    # Проверка правильности регистрации юзера и входа юзера
    def test_register_and_login(self):
        response = self.client.post('/register',
                                    {'email': 'usermail@test.ru', 'password1': 'Test12345', 'password2': 'Test12345'})
        login = self.client.post('/login', {'username': 'usermail@test.ru', 'password': 'Test12345'})

        self.assertTrue(response.status_code == 302 and login.status_code == 302)

    # проваленный тест логина
    def test_not_login(self):
        response = self.client.post('/register',
                                    {'email': 'usermail@test.ru', 'password1': 'Test12345', 'password2': 'Test12345'})
        login = self.client.post('/login', {'username': 'notusermail@test.ru', 'password': 'Test12345'})

        self.assertFalse(response.status_code == 302 and login.status_code == 302)


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Category.objects.create(name='Тестовая категория')

    def test_category_label(self):
        # тестирование правильности записи и получения имени
        category = Category.objects.get(id=1)
        field_label = category.name
        self.assertEquals(field_label, 'Тестовая категория')


class CycleModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Тестовая категория')
        Cycle.objects.create(title='Test Name of Cycle (2022)', description='Description of test cycle', price=22000,
                             category=Category.objects.get(id=1))

    def test_category_label(self):
        # тестирование правильности записи и возвращения названия категории
        category = Category.objects.get(id=1)
        field_label = category.name
        self.assertEquals(field_label, 'Тестовая категория')

    def test_cycle_label(self):
        # тестирование правильности записи и возвращения наименования велосипеда
        cycle = Cycle.objects.get(id=1)
        field_label = cycle.title
        self.assertEquals(field_label, 'Test Name of Cycle (2022)')

    def test_cycle_price(self):
        # тестирование правильности записи и возвращения цены велосипеда
        cycle = Cycle.objects.get(id=1)
        price = cycle.price
        self.assertEquals(price, 22000)
