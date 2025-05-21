from django.db import models
from django.contrib.auth.models import User
from datetime import date
import re
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

phone_regex = RegexValidator(
    regex=r'^\+375 \(29\) \d{3}-\d{2}-\d{2}$',
    message="Формат: +375 (29) XXX-XX-XX"
)
# Create your models here.
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(
        regex=r'^\+375 \(29\) \d{3}-\d{2}-\d{2}$',
        message="Формат: +375 (29) XXX-XX-XX"
    )
    phone_number = models.CharField(max_length=19, validators=[phone_regex])
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return (
            f"{self.user.get_full_name()}" 
            if self.user.first_name or self.user.last_name 
            else self.user.username
        )

    

class ParkingPlace(models.Model):
    number = models.PositiveIntegerField(unique=True, validators=[MaxValueValidator(999)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_occupied = models.BooleanField(default=False)
    def __str__(self):
        return f"Место {self.number}"
    
class Car(models.Model):
    owner = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='owned_cars')
    clients = models.ManyToManyField(Client, related_name='cars')
    license_plate = models.CharField(max_length=15, unique=True, db_index=True)
    model = models.CharField(max_length=100)
    parking_place = models.OneToOneField(
        ParkingPlace, 
        on_delete=models.PROTECT,  # Изменено с SET_NULL
        null=False,                # Запрещаем NULL
        blank=False               # Запрещаем пустое значение в формах
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        self.license_plate = self.normalize_plate(self.license_plate)
        super().save(*args, **kwargs)
    
    @staticmethod
    def normalize_plate(plate):
        return re.sub(r'[^A-Z0-9]', '', plate.upper())
    
    def __str__(self):
        return self.license_plate

class Invoice(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    car = models.ForeignKey(  # Новая связь с автомобилем
        'Car', 
        on_delete=models.CASCADE,
        verbose_name='Автомобиль',
        related_name='invoices'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_payment = models.BooleanField(default=False)  # False - начисление, True - оплата
    period = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Article(models.Model):
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class CompanyInfo(models.Model):
    name = models.CharField(max_length=200, default='')
    text = models.TextField(blank=True)
    # дополнительно: logo, video_url, history_year, requisites

    def __str__(self):
        return self.name or 'Информация о компании'
    
class Term(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question
    
class Employee(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='employees/')
    position = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name
    
class Vacancy(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв {self.name} ({self.rating})"
    
class PromoCode(models.Model):
    code = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.code