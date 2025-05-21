from django.contrib import admin
from django.db.models import Sum, Case, When, F, DecimalField, Count
from .models import Client, Car, ParkingPlace, Invoice, Article, CompanyInfo, Term, Employee, Vacancy, Review, PromoCode
from django.utils.html import format_html

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'birth_date', 'current_debt', 'last_payment')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    
    def current_debt(self, obj):
        debt = obj.invoice_set.aggregate(
            total=Sum(
                Case(
                    When(is_payment=True, then=-F('amount')),  # Исправлено здесь!
                    default=F('amount'),
                    output_field=DecimalField()
                )
            )
        )['total'] or 0
        return f"{debt:.2f} руб"  # Добавлено форматирование
    current_debt.short_description = 'Текущий долг'
    
    def last_payment(self, obj):
        last = obj.invoice_set.filter(is_payment=True).order_by('-created_at').first()
        return last.created_at if last else 'Нет платежей'
    last_payment.short_description = 'Последний платеж'

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'model', 'parking_place', 'owners_count', 'show_owners')
    search_fields = ('model',)
    list_filter = ('clients__id',)
    actions = ['show_owners_action']
    filter_horizontal = ('clients',)
    
    def owners_count(self, obj):
        return obj.clients.count()
    owners_count.short_description = 'Кол-во владельцев'
    
    def show_owners(self, obj):
        return format_html(", ".join([str(c) for c in obj.clients.all()]))
    show_owners.short_description = 'Владельцы'
    
    @admin.action(description="Показать владельцев выбранных авто")
    def show_owners_action(self, request, queryset):
        for car in queryset:
            self.message_user(request, f"{car}: {list(car.clients.all())}")

class PeriodFilter(admin.SimpleListFilter):
    title = 'Период долга'
    parameter_name = 'period'
    
    def lookups(self, request, model_admin):
        return (
            ('current_month', 'Текущий месяц'),
            ('last_month', 'Прошлый месяц'),
        )
    
    def queryset(self, request, queryset):
        return queryset

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('client', 'car','amount', 'created_at', 'is_payment', 'period', 'debt_status')
    list_filter = (PeriodFilter, 'period')
    
    def debt_status(self, obj):
        return "Оплата" if obj.is_payment else "Начисление"
    debt_status.short_description = 'Тип операции'

@admin.register(ParkingPlace)
class ParkingPlaceAdmin(admin.ModelAdmin):
    list_display = ('number', 'price', 'is_occupied')

admin.site.register(Article)
admin.site.register(CompanyInfo)
admin.site.register(Term)
admin.site.register(Employee)
admin.site.register(Vacancy)
admin.site.register(Review)
admin.site.register(PromoCode)