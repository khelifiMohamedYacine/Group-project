from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Location
from .forms import LocationForm

def map_view(request):
    """Render the map template."""
    return render(request, "locations/map.html")  # Ensure the path to your template is correct

@csrf_exempt
def add_location(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Received Data:", data) 
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            postcode = data.get('postcode')
            address = data.get('address')
            location_name = data.get('location_name')
            task1 = data.get('task1_id')  # Get task1
            task2 = data.get('task2_id')  # Get task2

            # Check if a location already exists with the same coordinates
            if Location.objects.filter(latitude=latitude, longitude=longitude).exists():
                return JsonResponse({"error": "Location with these coordinates already exists"}, status=400)

            # Save the new location, including tasks
            Location.objects.create(
                postcode=postcode,
                address=address,
                location_name=location_name,
                latitude=latitude,
                longitude=longitude,
                task1_id=task1 if task1 else None,  # Save only if provided
                task2_id=task2 if task2 else None   # Save only if provided
            )

            return JsonResponse({"success": "Location added successfully!"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

        
def get_locations(request):
    locations =locations = list(Location.objects.values(
        "postcode", 
        "latitude", 
        "longitude", 
        "task1_id", 
        "task2_id", 
        "location_name",  # Add location_name
        "locID"))
    return JsonResponse(locations, safe=False)

def delete_location_view(request):
    if request.method == "POST":
        selected_locations = request.POST.getlist('locations')  # Get the selected locIDs
        if selected_locations:
            # Delete the selected locations from the database
            Location.objects.filter(locID__in=selected_locations).delete()
        # After deleting, redirect back to the page or another page
        return redirect('delete_location')
    locations = Location.objects.all() 
    return render(request, 'locations/delete_location.html', {'locations': locations})

def location_list(request):
    locations = Location.objects.all()
    return render(request, 'locations/location_list.html', {'locations': locations})

def update_location(request, locID):
    location = get_object_or_404(Location, pk=locID)

    if request.method == "POST":
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return redirect('location_list')  # Redirect to the list after updating
    else:
        form = LocationForm(instance=location)

    return render(request, 'locations/location_form.html', {'form': form, 'location': location})


