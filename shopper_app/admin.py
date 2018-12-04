from django.contrib import admin

from .models import Item, GeoLoc, ItemLocation

admin.site.register(Item)
admin.site.register(GeoLoc)
admin.site.register(ItemLocation)