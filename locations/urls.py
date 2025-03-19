from django.urls import path
from . import views

app_name = "locations"

urlpatterns = [

    #FOR ADMIN
    path("game_admin/map", views.admin_map_view, name="admin_map_view"), #Add a location or view the existing locations on the map, with the button to generate a graph
    path("game_admin/delete-location/", views.delete_location_view, name="delete_location"), #Delete a location
    path('game_admin/update-location/', views.location_list, name='location_list'), #Update or edit a location
    path('game_admin/update-location/<int:locID>/', views.update_location, name='update_location'), #Update or edit a location by location ID (locID)

    #FOR USER
    path("map/", views.user_map_view, name="user_map_view"), #For users to view locations, their tasks and tasks status, along with the graph

    #FOR BACK-END
    path("add-location/", views.add_location, name="add_location"),
    path("get-locations/", views.get_locations, name="get_locations"),
    path('generate-graph/', views.generate_location_graph, name='generate_location_graph'),
    path('check-in/<int:loc_id>/', views.check_in, name='check_in'),
    path("get-locations-with-lock-status/", views.get_locations_with_lock_status, name="get_locations_with_lock_status"),

    path("get-task-ids/", views.get_task_ids, name="get_task_ids"),
]
