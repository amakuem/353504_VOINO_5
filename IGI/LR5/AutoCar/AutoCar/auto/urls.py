from django.urls import path
from  django.views.generic import  TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from . import views
from .views import CarCreateView, CarUpdateView, CarDeleteView, CarAttachView
from .views import ProfileView

urlpatterns = [
    path('', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('cars/new/', CarCreateView.as_view(), name='car_create'),
    path('cars/attach/', CarAttachView.as_view(), name='car_attach'),
    path('car/<int:pk>/edit/', CarUpdateView.as_view(), name='car_update'),
    path('car/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),
    path('set-timezone/', views.set_timezone, name='set_timezone'),
    path('set-timezone-auto/', views.set_timezone_auto, name='set_timezone_auto'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('about/', views.about, name='about'),
    path('news/', views.news_list, name='news_list'),
    path('terms/', views.terms, name='terms'),
    path('contacts/', views.contacts, name='contacts'),
    path('privacy/', views.privacy, name='privacy'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('reviews/', views.reviews, name='reviews'),
    path('promo/', views.promo_codes, name='promo_codes'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/clients/', views.client_list, name='client_list'),
    path('admin-dashboard/parking/', views.parking_list, name='parking_list'),
    path('admin-dashboard/top-debtor/', views.top_debtor, name='top_debtor'),
    path('admin-dashboard/multi-owners/', views.multi_owner_cars, name='multi_owners'),
    path('admin-dashboard/min-debt/', views.min_debt, name='min_debt'),
    path('admin-dashboard/total-debt/', views.total_debt, name='total_debt'),
    path('admin-dashboard/car-brand/', views.car_brand_search, name='car_brand'),
    path('services/', views.services_view, name='services'),
]