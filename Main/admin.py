from django.contrib import admin
from .models import Item, UserProfile, Order

admin.site.register(Item)
admin.site.register(UserProfile)
admin.site.register(Order)
