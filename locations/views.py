from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from core_app.models import UserAccount, AccountType
from .models import Location, UserLocation
from .forms import LocationForm
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from django.http import HttpResponse

from quizzes.models import Quiz
from sokoban_game.models import sokoban_level
from django.contrib.contenttypes.models import ContentType

page_forbidden_string = "You dont have permission to access this page. Only game admins do."

@login_required
def admin_map_view(request):
    if request.user.account_type != AccountType.ADMIN.value:
        return HttpResponseForbidden(page_forbidden_string)

    return render(request, "locations/map.html") 

@login_required
def user_map_view(request):
    return render(request, "locations/user_map.html") 

@login_required
@csrf_exempt
def add_location(request):
    if request.user.account_type != AccountType.ADMIN.value:
        return HttpResponseForbidden(page_forbidden_string)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Received Data:", data)

            latitude = data.get('latitude')
            longitude = data.get('longitude')
            address = data.get('address')
            location_name = data.get('location_name')
            locked_by = data.get('locked_by')

            # Handle task1 and task2 which are using GenericForeignKey
            task1_id = data.get('task1_id')
            task2_id = data.get('task2_id')
            task1_instance = None
            if task1_id:
                task1_type = data.get('task1_type')  # Get the task type for task1
                task1_content_type = ContentType.objects.get(model=task1_type.lower())  # Use ContentType to find model
                task1_instance = task1_content_type.get_object_for_this_type(id=task1_id)

            task2_instance = None
            if task2_id:
                task2_type = data.get('task2_type')  # Get the task type for task2
                task2_content_type = ContentType.objects.get(model=task2_type.lower())  # Use ContentType to find model
                task2_instance = task2_content_type.get_object_for_this_type(id=task2_id)

            if locked_by:
                # Attempt to get the location by locID
                locked_by = Location.objects.filter(locID=locked_by).first()
                if not locked_by: # validate locked by is a real location
                    return JsonResponse({"error": "Parent location does not exist"}, status=400)
            else:
                locked_by = None


            # Input Validation
            if (latitude == 9999 or longitude == 9999): # 9999 indicates that no position was selected by user
                return JsonResponse({"error": "Please select a location on the map"}, status=400)
            if not address:
                return JsonResponse({"error": "Please fill in all fields before adding the location. Missing Address."}, status=400)
            if not location_name:
                return JsonResponse({"error": "Please fill in all fields before adding the location. Missing Location Name."}, status=400)

            if Location.objects.filter(latitude=latitude, longitude=longitude).exists():
                return JsonResponse({"error": "Location with these coordinates already exists"}, status=400)
            try:
                latitude = float(latitude)
                longitude = float(longitude)
            except ValueError:
                return JsonResponse({"error": "Latitude and Longitude must be valid numbers."}, status=400)
            # Validate if latitude and longitude are within valid geographical ranges
            if not (-90 <= latitude <= 90):
                return JsonResponse({"error": "Latitude must be between -90 and 90."}, status=400)
            if not (-180 <= longitude <= 180):
                return JsonResponse({"error": "Longitude must be between -180 and 180."}, status=400)


            # Save the new location, including tasks
            print("locked_by:", locked_by)
            Location.objects.create(
                address=address,
                location_name=location_name,
                latitude=latitude,
                longitude=longitude,
                task1=task1_instance,
                task2=task2_instance,
                locked_by=locked_by,
            )

            return JsonResponse({"success": "Location added successfully!"}, status=201)

        except Exception as e:
            print("Error adding location: ", e)
            return JsonResponse({"error": str(e)}, status=400)

@login_required
def get_locations(request):
    locations =locations = list(Location.objects.values(
        "latitude", 
        "longitude", 
        "task1_id", 
        "task2_id", 
        "location_name",  
        "locID",
        "locked_by"))
    return JsonResponse(locations, safe=False)

@login_required
def get_locations_with_lock_status(request):
    locations = Location.objects.all()
    location_data = []

    user = request.user

    for loc in locations:
        user_location = UserLocation.objects.filter(userID=user, locationID=loc).first()

        is_checked_in = user_location.checked_in if user_location and user_location.checked_in else False

        is_locked = False
        status = ""

        # Check if location is locked
        if not loc.locked_by:                                                                 #if location isnt locked at all
            is_locked = False
        elif user_location is None:
            is_locked = False
        elif user_location.checked_in:                                                        #if user has already checked in
            is_locked = False
        else:
            parent_user_location = UserLocation.objects.filter(userID=user, locationID=loc.locked_by).first()
            if parent_user_location is None:                                                  #if user has not interacted with the parent object
                is_locked = True
            elif parent_user_location.task1_complete and parent_user_location.task2_complete: #if user has complete both tasks for the parent
                is_locked = False
            else:                                                                             #user has not completed both tasks
                is_locked = True

        if is_locked:
            status = "locked"  # Red marker
        elif not is_checked_in:
            status = "pending"  # Blue marker (unlocked but not checked-in)
        else:
            status = "completed"  # Green marker (checked-in)
        

        location_data.append({
            "locID": loc.locID,
            "latitude": loc.latitude,
            "longitude": loc.longitude,
            "location_name": loc.location_name,
            "checked_in": is_checked_in,
            "task1_id": loc.task1_id,
            "task2_id": loc.task2_id,
            "locked": is_locked,
            "status": status  # New field to determine marker color
        })
    return JsonResponse(location_data, safe=False)

@login_required
def delete_location_view(request):
    if request.user.account_type != AccountType.ADMIN.value:
        return HttpResponseForbidden(page_forbidden_string)

    if request.method == "POST":
        selected_locations = request.POST.getlist('locations')  # Get the selected locIDs
        if selected_locations:
            # Delete the selected locations from the database
            Location.objects.filter(locID__in=selected_locations).delete()
        # After deleting, redirect back to the page or another page
        return redirect('locations:delete_location')
    locations = Location.objects.all() 
    return render(request, 'locations/delete_location.html', {'locations': locations})

@login_required
def location_list(request):
    if request.user.account_type != AccountType.ADMIN.value:
        return HttpResponseForbidden(page_forbidden_string)
    locations = Location.objects.all()
    return render(request, 'locations/location_list.html', {'locations': locations})

@login_required
def update_location(request, locID):
    if request.user.account_type != AccountType.ADMIN.value:
        return HttpResponseForbidden(page_forbidden_string)

    location = get_object_or_404(Location, pk=locID)

    if request.method == "POST":
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return redirect('locations:location_list')  # Redirect to the list after updating
    else:
        form = LocationForm(instance=location)

    return render(request, 'locations/location_form.html', {'form': form, 'location': location})

@login_required
def generate_location_graph(request):
    # Create a directed graph
    G = nx.DiGraph()

    locations = Location.objects.all()

    # Add nodes to the graph
    for location in locations:
        G.add_node(location.locID, name=location.location_name)

    # Add edges based on locked_by relationships
    for location in locations:
        if location.locked_by:
            G.add_edge(location.locked_by, location.locID)

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='green', font_size=10, font_weight='bold', arrows=True)
   
    # Save the graph to a BytesIO object so it can be sent in HTTP response
    from io import BytesIO
    img_io = BytesIO()
    plt.savefig(img_io, format='PNG')
    img_io.seek(0)

    # Serve the image in HTTP response
    return HttpResponse(img_io, content_type='image/png')

@login_required
@csrf_exempt
def check_in(request, loc_id):
    if request.method == "POST":
        user = request.user
        try:
            location = Location.objects.get(locID=loc_id) 
            print(f"Location found: {location}")

            # Get or create a UserLocation entry for this user & location
            user_location, created = UserLocation.objects.get_or_create(
                userID=user,
                locationID=location,
                task1_complete = False,
                task2_complete = False,
                defaults={"checked_in": True}
            )
            if location.task1_id is None: # if there is no task imidiately set it to None
                user_location.task1_complete = True
            if location.task2_id is None:
                user_location.task2_complete = True
            location.save()  #
            
            if created:
                # a new entry was created, means the user wasn't checked in before
                return JsonResponse({'message': 'Check-in successful!', 'checked_in': True})
            else:
                # the entry already exists, means the user has already checked in
                return JsonResponse({'message': 'Already checked in.', 'checked_in': True})

        except Location.DoesNotExist:
            return JsonResponse({'error': 'Location not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)


def get_task_ids(request):
    # Returns data for the drop down menu

    if request.user.account_type != AccountType.ADMIN.value:
        return HttpResponseForbidden(page_forbidden_string)

    task_type = request.GET.get('task_type')
    print(f"Received task_type: {task_type}")
    
    if not task_type:
        return JsonResponse({'error': 'Task type is required'}, status=400)
    
    try:
        
        # Query the task model based on the task type
        if task_type == "Quiz":
            print("we got quiz")
            tasks = Quiz.objects.all().values_list("id", flat=True)
        elif task_type == "Jumping_Game":
            tasks = JumpingGame.objects.all().values_list("id", flat=True)
        elif task_type == "sokoban_level":
            print("we got here")
            tasks = sokoban_level.objects.all().values_list("id", flat=True)
        else:
            return JsonResponse({'error': 'Invalid task type'}, status=400)

        # Return task ids in the response
        return JsonResponse({'task_ids': list(tasks)}, status=200)

    except Exception as e:
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
