from django.urls import path
from . import views

urlpatterns = [
    path("", views.map_view, name="map_view"),  # This will render the template
    path("add-location/", views.add_location, name="add_location"),
    path("get-locations/", views.get_locations, name="get_locations"),

]
