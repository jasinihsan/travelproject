from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required 
from .models import TourPackage

class TourListView(ListView):
    model = TourPackage
    template_name = "tours/tour_list.html"
    context_object_name = "tours"

def tour_detail(request, tour_id):
    """Show details of a specific tour package."""
    tour = get_object_or_404(TourPackage, id=tour_id)
    return render(request, "tours/tour_detail.html", {"tour": tour})

def home(request):
    """Homepage showing all tours."""
    tours = TourPackage.objects.all()  
    return render(request, "tours/home.html", {"tours": tours})

@login_required
def add_tour(request):
    """View for adding a new tour package"""
    return render(request, "tours/add_tour.html")  
