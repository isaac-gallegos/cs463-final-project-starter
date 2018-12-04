import json
from django.urls import reverse_lazy
from django.http import JsonResponse

from django.conf import settings
from django import forms

# generic views docs: https://docs.djangoproject.com/en/2.1/ref/class-based-views/
from django.views import generic 

from .models import Item, GeoLoc, ItemLocation

# (e.g., HOME_LOC['latitude'] or HOME_LOC['longitude'])
HOME_LOC = settings.DEFAULT_LOC 

class HomeView(generic.TemplateView):
    template_name = 'home.html'


class ItemView(generic.DetailView):
    model = Item
    template_name = 'item.html'

    def get_context_data(self, **kwargs):
        context = super(ItemView, self).get_context_data(**kwargs)
        item_obj = self.get_object()
        
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
            'name': item name, 
            'price': item price, 
            'lat': item latitude, 
            'lon': longitude, 
            'image_url': item image url
        }

    miles:  number of miles required to fetch each item at each location. The
            total distance traversing the path of locations.

    total_cost: The total cost of all item objects selected in form. 
    """

    def post(self, request, *args, **kwargs):
        """Handle post requests from client form using AJAX.
        """
        form = SearchForm(request.POST)
        miles = 0       # total number miles to fetch all items
        total_cost = 0  # total cost of all items

        # data dict sent back to client as response 
        # Note: each item in items list should be a dict of the format
        # {'name': item name, 'price': item price, 'lat': item latitude, 'lon': longitude}
        data = {'items': [], 'miles': miles, 'cost': total_cost}

        if form.is_valid:
            # Extract selected items (checked items from form) and build list of item objects
            form_data = request.POST.getlist('items')
            item_objects = [] 
            for i in form_data:
                item_obj = Item.objects.get(pk=i)
                item_objects.append(item_obj)
        
            #  Begin here to determine optimal item location for each item in item_objects list


            # End local edits here.

        return JsonResponse(data, safe=False)
        



