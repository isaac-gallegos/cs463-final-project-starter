import json
from django.urls import reverse_lazy
from django.http import JsonResponse

from django.conf import settings
from django import forms

# generic views docs: https://docs.djangoproject.com/en/2.1/ref/class-based-views/
from django.views import generic 
from geopy import distance
from geopy import Nominatim

from .models import Item, GeoLoc, ItemLocation

# (e.g., HOME_LOC['latitude'] or HOME_LOC['longitude'])
HOME_LOC = settings.DEFAULT_LOC
d = distance.distance
g = Nominatim(user_agent="shopper_app")

class HomeView(generic.TemplateView):
    template_name = 'home.html'


class ItemView(generic.DetailView):
    model = Item
    template_name = 'item.html'

    def get_context_data(self, **kwargs):
        context = super(ItemView, self).get_context_data(**kwargs)
        item_obj = self.get_object()
        item_locations = item_obj.locations.all()
        context['locations'] = item_locations
        return context


class ItemListView(generic.ListView):
    model = Item
    template_name = 'item_list.html'


class ItemCreateView(generic.CreateView):
    model = Item                     # Object we want to create
    template_name = 'item_add.html'  # template that displays the form
    
    # list of attributes we want to display widgets for...
    fields = ['name', 'price', 'image_url']
    success_url = reverse_lazy('item_list')


class SearchForm(forms.Form):
    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), widget=forms.widgets.CheckboxSelectMultiple)


class SelectItemsView(generic.TemplateView):
    template_name = 'shop.html'

    def get_context_data(self, **kwargs):
        context = super(SelectItemsView, self).get_context_data(**kwargs)
        context['items'] = Item.objects.all()
        return context



# REST API # 
class ItemsResultsRestView(generic.View):
    """RESTful api to access item database.
    /shop/rest/ takes post data and returns json response containing
    item objects that are within minimal distance to a default location.

    response structure
    data = 
        {
        'items': [], 
        'miles': miles, 
        'cost': total_cost
        }

    items:  list of item objects that are minimal distance to origin.
        structure for each item object:
        
        {
            'name': item's name, 
            'price': item's price, 
            'lat': item's latitude, 
            'lon': item's longitude, 
            'image_url': item's image url
        }

    miles:  number of miles required to fetch each item at each location. The
            total distance traversing the path of locations.

    total_cost: The total cost of all item objects selected in form. 
    """

    def post(self, request, *args, **kwargs):
        """Handle post requests from client form using AJAX.
        """
        form = SearchForm(request.POST)
        a = (-71.312796, 41.49008)
        b = (-71.312796, 41.49008)
        miles = distance.distance(a, b).miles # total number miles to fetch all items. Also initializing variable miles as a geodesic type to perform geodesic logic

        total_cost = 0 # total cost of all items
        
        #initializing item dictionary's dictionary to properly send as a json response
        name = []
        price = 0
        lat = 0
        lon = 0

        # data dict sent back to client as response 
        data = {'items': [], 'miles': miles, 'cost': total_cost}
        # Note: each item in 'items' list is a dict in itself and should be structured as outlined above.

        if form.is_valid:
            # Extract selected items (checked items from form) and build list of item objects
            form_data = request.POST.getlist('items')
            item_objects = [] 
            for i in form_data:
                item_obj = Item.objects.get(pk=i)
                item_objects.append(item_obj)
        
            #  Begin here to determine optimal item location for each item in item_objects list

            home_coordinates = (HOME_LOC['latitude'], HOME_LOC['longitude'])
            for i in item_objects:
                locations = i.locations.all()
                min_location = (locations[0].location.lat, locations[0].location.lon)
                min_miles = distance.distance(min_location, home_coordinates)
                for j in locations:
                    location = (j.location.lat, j.location.lon)
                    new_distance = distance.distance(location, home_coordinates).miles
                    if new_distance < min_miles:
                        min_miles = new_distance
                        min_location = j
                data['items'].append({
                    'name': min_location.item.name, 
                    'price': min_location.item.price,
                    'lat': min_location.location.lat,
                    'lon': min_location.location.lon})
                data['miles'] = data['miles'] +new_distance
                data['cost'] = data['cost'] + min_location.item.price

            # End local edits here.
        return JsonResponse(data, safe=False)