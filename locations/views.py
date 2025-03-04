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
        data = json.loads(request.body)
        postcode = data.get("postcode")
        address = data.get("address")
        location_name = data.get("location_name")
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if postcode and address and location_name and latitude and longitude:
            Location.objects.create(
                postcode=postcode,
                address=address,
                location_name=location_name,
                latitude=latitude,
                longitude=longitude
            )
            return JsonResponse({"message": "Location saved successfully"}, status=201)

    return JsonResponse({"error": "Invalid data"}, status=400)

def get_locations(request):
    locations = list(Location.objects.values("postcode", "latitude", "longitude", "task1_id", "task2_id", "task3_id"))
    return JsonResponse(locations, safe=False)