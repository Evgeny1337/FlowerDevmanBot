from django.contrib import admin
from django.forms import ModelForm
from django import forms

from .models import Flower, Event, Order, CustomUser, BouquetOfFlowers, Consultation, ColorPalette


class EventAdminInline(admin.TabularInline):
    model = BouquetOfFlowers.events.through


class FlowerAdminInline(admin.TabularInline):
    model = BouquetOfFlowers.flowers.through


class ColorPaletteAdminInline(admin.TabularInline):
    model = BouquetOfFlowers.color_palette.through


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'bouquet_of_flowers' in self.initial:
            bouquet_of_flowers_id = self.initial['bouquet_of_flowers']
            self.fields['exclude_flowers'].queryset = BouquetOfFlowers.objects.get(
                id=bouquet_of_flowers_id).flowers.all()
        else:
            self.fields['exclude_flowers'].queryset = Flower.objects.none()


class BouquetOfFlowersForm(ModelForm):
    class Meta:
        model = BouquetOfFlowers
        fields = '__all__'

    binary_photo = forms.ImageField()


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'telegram_username']
    search_fields = ['username', 'telegram_username']


@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name', ]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name', ]


@admin.register(ColorPalette)
class ColorPaletteAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name', ]


@admin.register(BouquetOfFlowers)
class BouquetOfFlowersAdmin(admin.ModelAdmin):
    form = BouquetOfFlowersForm
    list_display = ['id', 'name', 'price']
    search_fields = ['name']
    list_filter = ['price', 'name']
    inlines = [EventAdminInline, FlowerAdminInline, ColorPaletteAdminInline]


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'created', 'status']
    list_editable = ['status', ]
    search_fields = ['customer__username']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
    list_display = ['id', 'customer', 'address', 'bouquet_of_flowers', 'delivery', 'status',
                    'total_price_with_currency']
    list_filter = ['delivery', 'status', 'bouquet_of_flowers']
    list_editable = ['status', ]
    search_fields = ['customer__username', 'address', 'bouquet_of_flowers__name']

    def total_price_with_currency(self, obj):
        return f"{obj.total_price} руб."

    total_price_with_currency.short_description = 'Общая стоимость'
