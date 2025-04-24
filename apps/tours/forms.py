from django import forms
from .models import TourPackage

class TourPackageForm(forms.ModelForm):
    class Meta:
        model = TourPackage
        fields = ['title', 'description', 'price', 'currency','duration', 'category', 'available_slots', 'expiry_date']
        
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }