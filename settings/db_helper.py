import django
from asgiref.sync import sync_to_async
import os
import sys
from django import setup
from datetime import datetime
child_directory = os.path.dirname(__file__)
parent_directory = os.path.dirname(child_directory)

sys.path.append(os.path.join(parent_directory,'flowers_shop'))
print('TEST',sys.path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flowers_shop.settings')

django.setup()


from flowers.models import Event, ColorPalette, BouquetOfFlowers, CustomUser, Consultation, Order


@sync_to_async
def get_actions():
    return list(Event.objects.all())

@sync_to_async
def get_colors():
    return list(ColorPalette.objects.all())

@sync_to_async
def get_money():
    return [bouquet['price'] for bouquet in BouquetOfFlowers.objects.values('price').distinct()]

@sync_to_async
def get_flowers_id(color, price, event):
    color = ColorPalette.objects.get(id=color)
    event = Event.objects.get(id=event)
    return [bouquet.id for bouquet in BouquetOfFlowers.objects.filter(price__lte=price, color_palette=color, events=event)]

@sync_to_async
def get_another_ids_flowers(id_list):
    return [bouquet.id for bouquet in BouquetOfFlowers.objects.exclude(id__in=id_list)]

@sync_to_async
def get_byid_flower(id):
    return BouquetOfFlowers.objects.get(id=id)

@sync_to_async
def get_ids_admins():
    return [user.telegram_id for user in CustomUser.objects.exclude(telegram_id=None)]

@sync_to_async
def save_consultations(phone_number):
    Consultation.objects.create(phone_number=phone_number)

@sync_to_async
def save_order(bouquet_id,address,datetime,phone_number):
    bouquet = BouquetOfFlowers.objects.get(id=bouquet_id)
    print(bouquet)
    order = Order()
    order.bouquet_of_flowers = bouquet
    order.delivery = datetime
    order.phone_number = phone_number
    order.total_price = bouquet.price
    order.address = address
    print(order)
    order.save()
    return order
