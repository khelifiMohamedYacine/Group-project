from django import forms
from .models import Location

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['location_name', 'task1_id', 'task2_id', 'postcode', 'address', 'locked_by', 'checked_in']  # Add address back

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get the current postcode and address values
        current_postcode = getattr(self.instance, 'postcode', '')
        current_address = getattr(self.instance, 'address', '')

        # Make fields read-only except postcode and address (conditionally)
        for field in ['latitude', 'longitude']:
            self.fields[field] = forms.CharField(
                initial=getattr(self.instance, field, ''), 
                disabled=True,
                required=False
            )

        # Make postcode editable only if it is "NOT AVAILABLE"
        if current_postcode != "NOT AVAILABLE":
            self.fields['postcode'] = forms.CharField(
                initial=current_postcode,
                disabled=True,  
                required=False
            )
        
        # Make address editable only if it is "Address not available"
        if current_address != "Address not available":
            self.fields['address'] = forms.CharField(
                initial=current_address,
                disabled=True,  
                required=False
            )
