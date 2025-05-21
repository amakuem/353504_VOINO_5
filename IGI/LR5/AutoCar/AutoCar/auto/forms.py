from django import forms
from .models import Car, Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import NumberInput

from .models import phone_regex

class ClientRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    phone_number = forms.CharField(
        max_length=19,
        validators=[phone_regex],
        help_text="Формат: +375 (29) XXX-XX-XX"
    )
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Укажите дату рождения"
    )

    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'first_name', 
            'last_name', 
            'password1', 
            'password2', 
            'phone_number', 
            'birth_date'
        ]


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['license_plate', 'model', 'parking_place']
        labels = {
            'parking_place': 'Парковочное место*'
        }
        help_texts = {
            'parking_place': 'Обязательное поле'
        }

    def clean_parking_place(self):
        parking_place = self.cleaned_data.get('parking_place')
        if parking_place.is_occupied:
            raise forms.ValidationError("Это парковочное место уже занято")
        return parking_place

class CarAttachForm(forms.Form):
    license_plate = forms.CharField(label='Номер автомобиля')

    def clean_license_plate(self):
        plate = self.cleaned_data['license_plate']
        normalized_plate = Car.normalize_plate(plate)
        car = Car.objects.filter(license_plate=normalized_plate).first()
        
        if not car:
            raise forms.ValidationError("Автомобиль с таким номером не найден")
        return car
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'rating', 'text']
        widgets = {
            'rating': NumberInput(attrs={
                'min': 1,
                'max': 5,
                'type': 'number'
            })
        }

class PeriodForm(forms.Form):
    start_date = forms.DateField(
        label='Начальная дата',
        input_formats=['%d.%m.%Y', '%Y-%m-%d'],  # Добавляем поддержку формата DD.MM.YYYY
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    end_date = forms.DateField(
        label='Конечная дата',
        input_formats=['%d.%m.%Y', '%Y-%m-%d'],
        widget=forms.DateInput(attrs={'type': 'date'})
    )

class CarBrandForm(forms.Form):
    brand = forms.CharField(label='Марка автомобиля', max_length=100)

class ParkingFilterForm(forms.Form):
    min_price = forms.IntegerField(
        label='Минимальная цена', 
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'От'})
    )
    max_price = forms.IntegerField(
        label='Максимальная цена', 
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'До'})
    )