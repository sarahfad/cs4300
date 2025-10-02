from django.db import models
from django.conf import settings

#Movie: title, description, release date, duration.
class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    release_date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")

    def __str__(self):
        return self.title
        
#Seat: seat number, booking status.
class Seat(models.Model):
    seat_number = models.CharField(max_length=3, unique=True)
    booking_status = models.BooleanField(default=False)

    def __str__(self):
        return self.seat_number

#Booking: movie, seat, user, booking date
class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="bookings") #link data across different models in this case booking and movie models
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    booking_date = models.DateTimeField(auto_now_add=True)

    #make sure people don't double book the same seat at the movie
    class Unique:
        unique_pair = ("movie", "seat")
    
    def __str__(self):
        return f"{self.user}->{self.movie} in {self.seat}"

