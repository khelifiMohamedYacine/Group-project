from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from core_app.models import UserAccount, AccountType
from .models import Location
from .forms import LocationForm
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from django.http import HttpResponse

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
            postcode = data.get('postcode')
            address = data.get('address')
            location_name = data.get('location_name')
            task1 = data.get('task1_id')
            task2 = data.get('task2_id')
            checked_in = data.get("checked_in", False) # default to false because it was causing errors and IDK what this is for

            locked_by = data.get("locked_by")
            if locked_by:
                # Convert locked_by from location name → Location object (if provided)
                locked_by = Location.objects.filter(location_name=locked_by).first()
                if not locked_by:
                    return JsonResponse({"error": "Parent location does not exist"}, status=400) #validate locked_by is a real loction in database
                #locked_by = locked_by.locID
            else:
                locked_by = None

            # Input Validation
            if not postcode:
                return JsonResponse({"error": "Please fill in all fields before adding the location. Missing Postcode."}, status=400)
            if not address:
                return JsonResponse({"error": "Please fill in all fields before adding the location. Missing Address."}, status=400)
            if not location_name:
                return JsonResponse({"error": "Please fill in all fields before adding the location. Missing Location Name."}, status=400)
            # somehow validate if the postcode is valid, assuming we dont just remove it from database

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
                postcode=postcode,
                address=address,
                location_name=location_name,
                latitude=latitude,
                longitude=longitude,
                task1_id=task1 if task1 else None,  # Save only if provided
                task2_id=task2 if task2 else None,  # Save only if provided
                locked_by=locked_by,
                checked_in=checked_in
            )

            return JsonResponse({"success": "Location added successfully!"}, status=201)

        except Exception as e:
            print("Error adding location: ", e)
            return JsonResponse({"error": str(e)}, status=400)

@login_required    
def check_parent_location(request, locID):
    # Check if the location exists
    location_exists = Location.objects.filter(locID=locID).exists()
    return JsonResponse({"exists": location_exists})

@login_required
def get_locations(request):
    locations =locations = list(Location.objects.values(
        "postcode", 
        "latitude", 
        "longitude", 
        "task1_id", 
        "task2_id", 
        "location_name",  
        #"locID",
        "locked_by",
        "checked_in"))
    return JsonResponse(locations, safe=False)

@login_required
def get_locations_with_lock_status(request):
    locations = Location.objects.all()
    location_data = []

    for loc in locations:
        # Determine lock status
        is_locked = False
        if loc.locked_by:
            parent_location = Location.objects.filter(locID=loc.locked_by.locID).first()
            if parent_location and not parent_location.checked_in:
                is_locked = True

        # Determine marker color based on task status
        if is_locked:
            status = "locked"  # Red marker
        elif not loc.checked_in:
            status = "pending"  # Blue marker (unlocked but not checked-in)
        else:
            status = "completed"  # Green marker (checked-in)

        location_data.append({
            "locID": loc.locID,
            "postcode": loc.postcode,
            "latitude": loc.latitude,
            "longitude": loc.longitude,
            "location_name": loc.location_name,
            "checked_in": loc.checked_in,
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
        return redirect('delete_location')
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

    if request.user.account_type != AccountType.ADMIN.value:
        return HttpResponseForbidden(page_forbidden_string)

    location = get_object_or_404(Location, pk=locID)

    if request.method == "POST":
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return redirect('location_list')  # Redirect to the list after updating
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
        try:
            location = Location.objects.get(locID=loc_id) 
            print(f"Location found: {location}")
            
            if not location.checked_in:
                location.checked_in = True
                location.save()
                return JsonResponse({'message': 'Check-in successful!', 'checked_in': True})
            else:
                return JsonResponse({'message': 'Already checked in.', 'checked_in': True})
        except Location.DoesNotExist:
            return JsonResponse({'error': 'Location not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)