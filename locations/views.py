from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Location

def map_view(request):
    """Render the map template."""
    return render(request, "locations/map.html")  # Ensure the path to your template is correct

@csrf_exempt
def add_location(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            postcode = data.get('postcode')
            address = data.get('address')
            location_name = data.get('location_name')

            # Check if a location already exists with the same coordinates
            if Location.objects.filter(latitude=latitude, longitude=longitude).exists():
                return JsonResponse({"error": "Location with these coordinates already exists"}, status=400)

            # Save the new location
            Location.objects.create(
                postcode=postcode,
                address=address,
                location_name=location_name,
                latitude=latitude,
                longitude=longitude
            )

            return JsonResponse({"success": "Location added successfully!"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
def get_locations(request):
    locations = list(Location.objects.values("postcode", "latitude", "longitude", "task1_id", "task2_id", "task3_id"))
    return JsonResponse(locations, safe=False)