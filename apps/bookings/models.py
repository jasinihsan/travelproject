from django.db import models
from apps.tours.models import TourPackage
from apps.accounts.models import CustomUser

class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tour = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
    num_people = models.PositiveIntegerField(default=1) 
    booking_date = models.DateTimeField(auto_now_add=True) 
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, 
        choices=[("pending", "Pending"), ("confirmed", "Confirmed")],
        default="pending"
    )

    def __str__(self):
        return f"Booking by {self.user.username} for {self.tour.title}" 
    
    
    def total_price(self):
        """Calculate total price based on number of people."""
        return self.num_people * self.tour.price