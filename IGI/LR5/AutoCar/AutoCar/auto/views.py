from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .forms import ClientRegistrationForm, CarCreateForm, CarAttachForm, ReviewForm, PeriodForm, CarBrandForm, ParkingFilterForm
from .models import  Client, Invoice, Car, ParkingPlace, Article, CompanyInfo, Term, Employee, Vacancy, Review, PromoCode, models
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, View,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.http import Http404, JsonResponse
import requests
from django.conf import settings
import pytz
import calendar
from django.views.decorators.http import require_http_methods
import numpy as np
import matplotlib
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Q
matplotlib.use('Agg')  # Важно для работы в Django
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import json
# Create your views here.


@require_http_methods(["POST"])
def set_timezone_auto(request):
    try:
        data = json.loads(request.body)
        tz = data.get('timezone')
        if tz in pytz.all_timezones:
            request.session['timezone'] = tz
            return JsonResponse({'status': 'ok'})
        return JsonResponse({'status': 'invalid timezone'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error'}, status=400)

def get_timezone_by_ip(request):
    """Определение временной зоны только по IP без дефолтных значений"""
    try:
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '127.0.0.1')).split(',')[0]
        response = requests.get(f'http://ip-api.com/json/{ip}?fields=timezone', timeout=3)
        if response.status_code == 200:
            return response.json().get('timezone')
    except Exception as e:
        print(f"Error getting timezone by IP: {e}")
    return None  # Всегда возвращаем None при ошибках

def get_client_timezone(request):
    tz_name = request.session.get('timezone')
    
    if not tz_name:
        # Пытаемся определить по IP, если не получается - оставляем UTC
        tz_name = get_timezone_by_ip(request) or 'UTC'
        request.session['timezone'] = tz_name
    
    return pytz.timezone(tz_name)

@require_http_methods(["GET", "POST"])
def set_timezone(request):
    if request.method == 'POST':
        try:
            tz = request.POST.get('timezone')
            if tz in pytz.all_timezones:
                request.session['timezone'] = tz
                messages.success(request, "Временная зона обновлена")
            else:
                messages.error(request, "Неверная временная зона")
        except Exception as e:
            messages.error(request, "Ошибка обновления временной зоны")
        return redirect('set_timezone')
    
    current_tz = request.session.get('timezone', 'UTC')  # Дефолтное значение UTC
    return render(request, 'timezone_form.html', {
        'timezones': pytz.all_timezones,
        'current_timezone': current_tz
    })

def index(request):
    weather_data = None
    joke_data = None
    client_tz = get_client_timezone(request)
    now_utc = timezone.now()
    now_local = now_utc.astimezone(client_tz)

    try:
        weather_response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q=Minsk&units=metric&appid={settings.OPENWEATHER_API_KEY}',
            timeout=5
        )
        if weather_response.status_code == 200:
            weather_data = weather_response.json()
    except requests.exceptions.RequestException:
        pass

    try:
        joke_response = requests.get(
            'https://official-joke-api.appspot.com/random_joke',
            timeout=5
        )
        if joke_response.status_code == 200:
            joke_data = joke_response.json()
    except requests.exceptions.RequestException:
        pass

    # Формируем контекст
    context = {
        'weather': weather_data,
        'joke': joke_data,
        'utc_date': now_utc.strftime("%d/%m/%Y"),
        'local_date': now_local.strftime("%d/%m/%Y"),
        'timezone': str(client_tz),
        'text_calendar': calendar.TextCalendar().formatmonth(
            now_local.year, 
            now_local.month
        ),
    }
    
    return render(request, 'index.html', context)

    

def register(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            
            Client.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone_number'],
                birth_date=form.cleaned_data['birth_date']
            )
            
            login(request, user)
            return redirect('/')  # Замените на ваш URL
    else:
        form = ClientRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

class ProfileView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'profile.html'
    context_object_name = 'client'

    def get_object(self):
        return self.request.user.client  # Получаем Client через User
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invoices'] = Invoice.objects.filter(client=self.object)
        return context
    

class CarCreateView(LoginRequiredMixin, CreateView):
    form_class = CarCreateForm
    template_name = 'car_create.html'
    
    def form_valid(self, form):
        client = self.request.user.client
        try:
            with transaction.atomic():
                # Создаем новый автомобиль
                car = form.save(commit=False)
                car.owner = client
                car.save()
                car.clients.add(client)

                # Обновляем статус парковочного места
                if car.parking_place:
                    car.parking_place.is_occupied = True
                    car.parking_place.save()
                    next_month = timezone.now() + relativedelta(months=1)
                    period = next_month.date().replace(day=1)
                    
                    Invoice.objects.create(
                        client=car.owner,
                        car=car,
                        amount=car.parking_place.price,
                        period=period,
                        is_payment=False
                    )
                messages.success(self.request, "Новый автомобиль успешно зарегистрирован")
                return redirect('profile')

        except IntegrityError:
            messages.error(self.request, "Этот номер уже занят, используйте форму привязки")
            return self.form_invalid(form)

class CarAttachView(LoginRequiredMixin, FormView):
    form_class = CarAttachForm
    template_name = 'car_attach.html'
    
    def form_valid(self, form):
        client = self.request.user.client
        car = form.cleaned_data['license_plate']
        
        if car.clients.filter(pk=client.pk).exists():
            messages.info(self.request, "Этот автомобиль уже привязан к вашему аккаунту")
        else:
            car.clients.add(client)
            messages.success(self.request, "Автомобиль успешно привязан")
        
        return redirect('profile')
    
class OwnerRequiredMixin(LoginRequiredMixin):
    """Миксин для проверки прав владельца автомобиля"""
    def dispatch(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            if self.object.owner != request.user.client:
                messages.error(request, "У вас нет прав для редактирования этого автомобиля")
                return redirect('profile')
            return super().dispatch(request, *args, **kwargs)
        except Http404:
            messages.error(request, "Автомобиль не найден")
            return redirect('profile')

class CarUpdateView(OwnerRequiredMixin, UpdateView):
    model = Car
    form_class = CarCreateForm
    template_name = 'car_form.html'
    success_url = reverse_lazy('profile')

    def get_queryset(self):
        """Показываем автомобили, где пользователь является владельцем"""
        return Car.objects.filter(owner=self.request.user.client)

    def get_object(self, queryset=None):
        """Получаем объект с обработкой 404 ошибки"""
        try:
            return super().get_object(queryset)
        except Http404:
            messages.error(self.request, "Автомобиль не найден или у вас нет прав доступа")
            raise

class CarDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        client = request.user.client
        
        if car.owner == client:
            # Освобождаем парковочное место
            if car.parking_place:
                car.parking_place.is_occupied = False
                car.parking_place.save()
            car.delete()
            messages.success(request, "Автомобиль полностью удален")
        else:
            car.clients.remove(client)
            messages.success(request, "Вы отвязаны от автомобиля")
        
        return redirect('profile')
    
def statistics_view(request):
    # Получаем всех клиентов
    clients = Client.objects.all()
    
    # Рассчитываем возрасты
    today = timezone.now().date()
    ages = []
    for client in clients:
        if client.birth_date:
            age = (today - client.birth_date).days // 365
            ages.append(age)
    
    # Рассчитываем статистику
    stats = {
        'total_clients': len(ages),
        'avg_age': round(np.mean(ages), 2) if ages else 0,
        'median_age': round(np.median(ages), 2) if ages else 0,
    }
    
    # Создаем график
    plt.figure(figsize=(10, 6))
    
    # Гистограмма распределения возрастов
    if ages:
        n, bins, patches = plt.hist(ages, bins=10, edgecolor='black')
        plt.xlabel('Возраст')
        plt.ylabel('Количество клиентов')
        plt.title('Распределение возрастов клиентов')
    
    # Сохраняем график в base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    graphic = base64.b64encode(image_png).decode('utf-8')
    plt.close()
    
    return render(request, 'statistics.html', {
        'stats': stats,
        'graphic': graphic,
    })

def about(request):
    """О компании"""
    info = CompanyInfo.objects.first()
    return render(request, 'about.html', {'info': info})

def news_list(request):
    """Список новостей"""
    articles = Article.objects.order_by('-published_at')
    return render(request, 'news_list.html', {'articles': articles})

def terms(request):
    """Словарь терминов и понятий"""
    terms = Term.objects.order_by('-added_at')
    return render(request, 'terms.html', {'terms': terms})

def contacts(request):
    """Контакты сотрудников"""
    employees = Employee.objects.all()
    return render(request, 'contacts.html', {'employees': employees})

def privacy(request):
    """Политика конфиденциальности"""
    return render(request, 'privacy.html')

def vacancies(request):
    """Список вакансий"""
    vacs = Vacancy.objects.order_by('-posted_at')
    return render(request, 'vacancies.html', {'vacancies': vacs})

def promo_codes(request):
    """Промокоды и купоны"""
    codes = PromoCode.objects.order_by('-created_at')
    return render(request, 'promo_codes.html', {'codes': codes})

def reviews(request):
    reviews_qs = Review.objects.order_by('-created_at')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rev = form.save(commit=False)
            if request.user.is_authenticated:
                # подставляем username в ревью и связываем пользователя
                rev.user = request.user
                rev.name = request.user.username
            rev.save()
            return redirect('reviews')
    else:
        # при GET сразу создаём форму с initial для name
        if request.user.is_authenticated:
            form = ReviewForm(initial={'name': request.user.username})
            # сделаем поле только для чтения, чтобы юзер не менял имя:
            form.fields['name'].widget.attrs['readonly'] = True
        else:
            form = ReviewForm()

    return render(request, 'reviews.html', {
        'reviews': reviews_qs,
        'form': form,
    })


@staff_member_required
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')
@staff_member_required
def client_list(request):
    clients = Client.objects.all().annotate(
        total_debt=Sum('invoice__amount', filter=Q(invoice__is_payment=False)))
    return render(request, 'admin/clients.html', {'clients': clients})

@staff_member_required
def parking_list(request):
    if request.method == 'POST':
        place_id = request.POST.get('place_id')
        new_price = request.POST.get('price')
        place = ParkingPlace.objects.get(id=place_id)
        place.price = new_price
        place.save()
        messages.success(request, 'Цена обновлена')
    
    # Добавляем подсчет занятых мест
    places = ParkingPlace.objects.select_related('car').all()
    total_occupied = places.filter(is_occupied=True).count()
    
    return render(request, 'admin/parking.html', {
        'places': places,
        'total_occupied': total_occupied
    })

# views.py
@staff_member_required
def top_debtor(request):
    # Получаем клиента с максимальным долгом
    clients = Client.objects.annotate(
        total_debt=Sum('invoice__amount', filter=Q(invoice__is_payment=False))
    ).order_by('-total_debt')[:1]

    client = clients[0] if clients else None
    last_payment = None
    
    if client:
        last_payment = Invoice.objects.filter(
            client=client, 
            is_payment=True
        ).order_by('-created_at').first()

    return render(request, 'admin/top_debtor.html', {
        'client': client,
        'last_payment': last_payment
    })

@staff_member_required
def multi_owner_cars(request):
    # Автомобили с несколькими владельцами
    cars = Car.objects.annotate(
        owners_count=Count('clients')
    ).filter(owners_count__gt=1)
    
    return render(request, 'admin/multi_owners.html', {'cars': cars})

# views.py
@staff_member_required
def min_debt(request):
    form = PeriodForm(request.GET or None)
    context = {'form': form}
    
    if form.is_valid():
        start = form.cleaned_data['start_date']
        end = form.cleaned_data['end_date']
        
        # Исправленный запрос с правильным related_name
        cars = Car.objects.annotate(
            total_debt=Sum('invoices__amount',  # Используем правильный related_name
                         filter=Q(
                             invoices__period__range=(start, end),
                             invoices__is_payment=False)
            )
        ).exclude(total_debt__isnull=True).order_by('total_debt')[:1]
        
        context['car'] = cars[0] if cars else None
    
    return render(request, 'admin/min_debt.html', context)

@staff_member_required
def total_debt(request):
    form = PeriodForm(request.GET or None)
    total = 0
    context = {'form': form}
    
    if form.is_valid():
        start = form.cleaned_data['start_date']
        end = form.cleaned_data['end_date']
        
        # Рассчитываем сумму всех начислений и платежей за период
        invoices = Invoice.objects.filter(
            Q(period__gte=start) & Q(period__lte=end)
        ).aggregate(
            total_charges=Sum('amount', filter=Q(is_payment=False)),
            total_payments=Sum('amount', filter=Q(is_payment=True))
        )
        
        charges = invoices['total_charges'] or 0
        payments = invoices['total_payments'] or 0
        total = charges - payments
        
        context.update({
            'total': total,
            'start_date': start,
            'end_date': end,
            'charges': charges,
            'payments': payments
        })
    
    return render(request, 'admin/total_debt.html', context)

@staff_member_required
def car_brand_search(request):
    # Поиск по марке автомобиля
    form = CarBrandForm(request.GET or None)
    cars = []
    if form.is_valid():
        brand = form.cleaned_data['brand']
        cars = Car.objects.filter(
            model__icontains=brand
        ).select_related('owner')
    
    return render(request, 'admin/car_brand.html', {
        'cars': cars,
        'form': form
    })

@staff_member_required
def admin_dashboard(request):
    # Ссылки для навигации по админ-панели
    menu = [
        {'url': 'client_list', 'name': 'Клиенты'},
        {'url': 'parking_list', 'name': 'Парковочные места'},
        {'url': 'top_debtor', 'name': 'Топ должник'},
        {'url': 'multi_owners', 'name': 'Авто с несколькими владельцами'},
        {'url': 'min_debt', 'name': 'Минимальный долг'},
        {'url': 'total_debt', 'name': 'Общий долг'},
        {'url': 'car_brand', 'name': 'Поиск по марке авто'},
    ]
    return render(request, 'admin/dashboard.html', {'menu': menu})

def services_view(request):
    form = ParkingFilterForm(request.GET or None)
    places = ParkingPlace.objects.filter(is_occupied=False)
    
    if form.is_valid():
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        
        if min_price:
            places = places.filter(price__gte=min_price)
        if max_price:
            places = places.filter(price__lte=max_price)

    return render(request, 'services.html', {
        'places': places,
        'form': form
    })