# cs463 Final Project Starter Code

## Overview
For this final assignment you will modify an existing Django web application by implementing backend application logic and frontend display and manipulation. The existing web application is based on the [shopping list](https://github.com/rmedinahu/cs463-django-sl-01) project we have been looking at for the last half of the semester. For the current extension, you will implement a page that shows selected items by the user that are within a minimal distance from Las Vegas NM (the origin). Items in the db are mapped to locations such that any given item can be located in 1 or more locations. The goal is to retrieve locations of items that are closest to the origin. In addition, these minimal locations are to be plotted (marked) in a map on the client browser. The following tasks will help you break down the necessary modifications to achieve the intended result.

## Submission

### Due in your repository by Friday Dec 14 by 11:59p. (I will clone/download whatever state your code is in at that time).
Be sure that you are consistently adding, committing, and pushing your changes to your github repo.

## Tasks

### Project Setup

* Create a virtual enviroment for this project on your development machine and make sure it is activated. (**Python 3 required**)

* Fork this Django project to your GH account then clone **your** fork to your development machine.

* CD to project root and run the following commands to prepare the application for development.

    * In your virtual environment install the package (Django, Geopy, etc.) requirements: 

    > pip install -r requirements.txt

    * Create the necessary db tables for the application: 

    > python manage.py migrate

    * Create a superuser account: 

    > python manage.py createsuperuser

    * Prepopulate application with existing data stored in a fixture: 

    > python manage.py loaddata shopper_app/fixtures/shopper_app_fixture.json

    * Start the Django development server: 

    > python manage.py runserver


### A. Modify Backend - ```ItemView```
Modify the ```get_context_data()``` method in [ItemView](https://github.com/rmedinahu/cs463-final-project-starter/blob/master/shopper_app/views.py#L20) to add a list of locations for the item to the context dict. Then modify the ```item.html``` template to display this list of locations. Display the ```city``` attribute for each location.

### B. Modify Backend - ```ItemsResultsRestView```
The relevant view to edit for this assignment is [ItemsResultsRestView](https://github.com/rmedinahu/cs463-final-project-starter/blob/master/shopper_app/views.py#L55). Your task is to implement the application logic in order to: 

a. Retrieve the minimal distance between each item object in the ```item_objects``` list and our default origin (see ```HOME_LOC``` variable in views.py) to produce a **NEW** list of ```ItemLocation``` objects that are of minimal distance to origin. **Use geopy and Nominatum python package for computing distance.**

> Be sure to use 'class project' for the ```user-agent``` attribute for the Nominatum constructor.

#### Helpful Hints:

- To get a list of ```ItemLocation``` associations for an Item object use the ```related_name``` attribute. If ```item_obj``` is a "Grape", here are its related locations

```python
item_locations = item_obj.locations.all()
```

- Each ```ItemLocation``` object has a ```location``` attribute that in turn has a ```lat``` and ```lon``` attribute.
    
- Grapes are located at six locations

```python
for item_loc in item_locations:
   print('item: ', item_loc.item.name)
   print('city: ', item_loc.location.city)
   print('(latitude, longitude): ', item_loc.location.lat, item_loc.location.lon)
   print('\n')
 
item:  Grape
city:  Gallup
(latitude, longitude):  35.38 -108.8

item:  Grape
city:  Ranchos De Taos
(latitude, longitude):  36.36 -105.6

item:  Grape
city:  Villanueva
(latitude, longitude):  35.26 -105.36

item:  Grape
city:  Tres Piedras
(latitude, longitude):  36.64 -105.96

item:  Grape
city:  Hagerman
(latitude, longitude):  33.11 -104.32

item:  Grape
city:  Paguate
(latitude, longitude):  35.1 -107.38

```

- If you can retrieve latitude and longitude you can compute distances using [geopy](https://geopy.readthedocs.io/en/stable/#module-geopy.distance)

b. From your list of minimal distance item_locations calculate the total miles required to visit each location.

c. From your list of item_locations calculate the total cost of the selected items.

d. Properly construct the ```data``` dict to send as response to client.

If the view properly sends data back to client, then the following modification to the frontend should result in the intended result.

### C. Modify Frontend 
1. Modify the menu bar in ```base.html``` to add a link to the 'admin' site. The url for admin is ```/admin/```.
2. Add the correct url pattern in ```urls.py``` so that ```shop/``` displays the shop.html page. Be sure to give it a 'name'. Use view ```SelectItemsView```

3. Modify the menu bar in ```base.html``` so that the shop menu option accesses the shop.html page (use pattern you created above).

4. Modify ```shop.html``` by completing the form that lists all the items in the db in a checklist. Each checklist item should use the primary key value for each item. For example, the pk of one of the items has a value of 2. Its checkbox ```value``` would be set as follows. Note that the ```name``` attribute of all checkbox items should be **items**. You can retrieve the pk by inspecting the admin site listing of item objects.

```html
<input type="checkbox" name="items" value="3">
```

5. The ```shop.html``` page is already started for you. Interaction unfolds like this: User selects items from checklist then clicks submit. On submit, the page makes an AJAX request to the ```ItemsResultsRestView``` you modified in task B (see javascript in page source). Modify the **response handler** to plot map locations in a map display **and** display the items (name and price) in a list on the page. 

> see [in class mapper exercise](https://github.com/rmedinahu/cs463-final-project-starter/blob/master/examples/mapper-article.html) to review dom manipulation and mapping

> see [in class NYT exercise](https://github.com/rmedinahu/cs463-final-project-starter/blob/master/examples/nytimes_lookup_solution.html) to review more dom manipulation techniques

* The AJAX Response from server should return the optimal location (latitude, longitude) for each selected **item information**, **total cost of selected items**, and **total miles required to visit each location**. Consult the structure below.

#### The structure of the json response:

```python
"""
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

```

### Sanity Check
Be sure your application is correctly displaying the selected items that are closest to origin. If the map is setup correctly one should be able to ascertain this by visual inspection.

## Relevant JavaScript Reference

### JavaScript Reference
- https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Client-side_web_APIs

- https://www.w3schools.com/jsref/

### Checkbox
- https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/checkbox

### AJAX
- https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch

- In class example [NY Times third pary api](https://github.com/rmedinahu/cs463-final-project-starter/blob/master/examples/nytimes_lookup_solution.html)

### Django
- https://docs.djangoproject.com/en/2.1/

### Geopy
- [geopy docs](https://geopy.readthedocs.io/en/stable/#)

- [geopy calculating distance](https://geopy.readthedocs.io/en/stable/#module-geopy.distance)

### Mapping
- https://leafletjs.com/

- In class example [Mapping and NYTimes lookup using Leaflet and NYT third party apis](https://github.com/rmedinahu/cs463-final-project-starter/blob/master/examples/mapper-article.html)


