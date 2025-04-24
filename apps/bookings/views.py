from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from .forms import BookingForm
from apps.tours.models import TourPackage
from apps.payments.models import Payment

@login_required
def book_tour(request, tour_id):
    tour = get_object_or_404(TourPackage, id=tour_id)

    if request.user.user_type != 'customer':
        messages.error(request, "You are not allowed to book a tour.")
        return redirect('home')

    form = BookingForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        booking = form.save(commit=False)
        booking.user = request.user
        booking.tour = tour
        booking.num_people = form.cleaned_data.get('num_people', 1)
        booking.total_price = tour.price * booking.num_people
        booking.save()

        
        payment = Payment.objects.create(
            user=request.user,
            booking=booking,
            amount=booking.total_price,
            method='cod',  
            status='pending'
        )

       
        return redirect('payments:make_payment', payment_id=payment.id)

    return render(request, "bookings/book_tour.html", {"form": form, "tour": tour})



@login_required
def vendor_bookings(request):
    """Displays Bookings for Vendor's Tours."""
    if request.user.user_type != "vendor":  
        messages.error(request, "Unauthorized access!")
        return redirect("home")  

   
    vendor_packages = TourPackage.objects.filter(vendor=request.user)

    
    bookings = Booking.objects.filter(tour__in=vendor_packages).order_by("-booking_date")

    return render(request, "bookings/vendor_booking_list.html", {"bookings": bookings})

@login_required
def user_bookings(request):
    """Displays Bookings for Logged-in Customer."""
    if request.user.user_type != "customer":
        messages.error(request, "Unauthorized access!")
        return redirect("home")

    bookings = Booking.objects.filter(user=request.user).order_by("-booking_date")
    return render(request, "bookings/user_bookings.html", {"bookings": bookings})

@login_required
def vendor_home(request):
    """Vendor Dashboard."""
    if request.user.user_type != "vendor":
        messages.error(request, "Unauthorized access!")
        return redirect("home")

    return render(request, "bookings/vendor_home.html")

@login_required
def booking_home(request):
    """Booking Home Page (Lists All Tour Packages)."""
    tours = TourPackage.objects.all()
    return render(request, "bookings/booking_home.html", {"tours": tours})

