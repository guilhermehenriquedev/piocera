from django.contrib import admin
from .models import Lot, LotModel, PaymentHistory, Order, AccountBank


@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_modality', 'name', 'price', 'start_date', 'end_date']
    list_display_links = ['id']
    search_fields = ['name']
    list_editable = ['category_modality', 'name', 'price', 'start_date', 'end_date']


@admin.register(LotModel)
class LotModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity_lots', 'price', 'percentage_accretion']
    list_display_links = ['name']
    search_fields = ['name']


@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name','order', 'billing_type', 'split_condictions', 'created_at', 'transaction_status', 'amount',
                    'invoice_url']

    list_display_links = ['id', 'order', 'billing_type', ]
    search_fields = ['order__registration__registration_number']
    save_on_top = True
    def user_name(self, obj):
        registration = obj.order.registration
        competitor_registration = registration.competitorsregistration_set.all()
        names = []
        for competitor in competitor_registration:
            names.append(f'{competitor.user.first_name} {competitor.user.last_name}')
        return names
    user_name.short_description = 'Usuário'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user_name','registration', 'status', 'lot', ]
    search_fields = ['registration__registration_number']
    def user_name(self, obj):
        registration = obj.registration
        competitor_registration = registration.competitorsregistration_set.all()
        names = []
        for competitor in competitor_registration:
            names.append(f'{competitor.user.first_name} {competitor.user.last_name}')
        return names
    user_name.short_description = 'Usuário'


@admin.register(AccountBank)
class AccountBankAdmin(admin.ModelAdmin):
    pass
