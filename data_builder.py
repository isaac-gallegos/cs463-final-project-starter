from shopper_app.models import *
from random import randint

items = Item.objects.all()
locs = GeoLoc.objects.all()
loc_limit = 6
loc_count = locs.count()

ilocs = ItemLocation.objects.all()
ilocs.delete()

for i in items:
   rlocs = randint(2, loc_limit)
   for j in range(rlocs):
     loc_idx = randint(0, loc_count)
     iloc = ItemLocation(item=i, location=locs[loc_idx])
     iloc.save()

ilocs = ItemLocation.objects.all()
print(ilocs.count())
