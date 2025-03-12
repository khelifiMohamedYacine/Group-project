from django.urls import path
from . import views

urlpatterns = [

    #FOR ADMIN
    path("", views.map_view, name="map_view"), #Add a location or view the existing locations on the map, with the button to generate a graph
    path("delete-location/", views.delete_location_view, name="delete_location"), #Delete a location
    path('update-location/', views.location_list, name='location_list'), #Update or edit a location
    path('update-location/<int:locID>/', views.update_location, name='update_location'), #Update or edit a location by location ID (locID)

    #FOR USER
    path("user-map/", views.user_map_view, name="user_map_view"), #For users to view locations, their tasks and tasks status, along with the graph

    #FOR BACK-END
    path("add-location/", views.add_location, name="add_location"),
    path("get-locations/", views.get_locations, name="get_locations"),    
    path('check-location/<int:locID>/', views.check_parent_location, name='check_parent_location'),
    path('generate-graph/', views.generate_location_graph, name='generate_location_graph'),
    path('check-in/<int:loc_id>/', views.check_in, name='check_in'),
    path("get-locations-with-lock-status/", views.get_locations_with_lock_status, name="get_locations_with_lock_status"),
   
]
