from django.db import models
from django.conf import settings
# (e.g., HOME_LOC['latitude'] or HOME_LOC['longitude'])
HOME_LOC = settings.DEFAULT_LOC

class GeoLoc(models.Model):
    postal_code = models.IntegerField(unique=True)
    city = models.CharField(max_length=128)
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return self.city


class Item(models.Model):
    name = models.CharField(max_length=128)
    price = models.IntegerField()
    image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name  # returns a string rep of the object


class ItemLocation(models.Model):
    """Associates an item with a location. An item can be found in multiple locations.
    """
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='locations')
    location = models.ForeignKey(GeoLoc, on_delete=models.CASCADE, related_name='items')

    class Meta:
        unique_together = (('location', 'item'),)






