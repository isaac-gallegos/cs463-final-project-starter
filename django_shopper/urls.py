"""django_shopper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from shopper_app.views import HomeView, ItemListView, ItemView, ItemCreateView, SelectItemsView, ItemsResultsRestView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('items/', ItemListView.as_view(), name='item_list'),
    path('item/<int:pk>/', ItemView.as_view(), name='item'),
    path('item/add/', ItemCreateView.as_view(), name='item_add'),
    
    # REST api
    path('shop/rest/', ItemsResultsRestView.as_view(), name='items_rest'),
    
    path('admin/', admin.site.urls),
]
