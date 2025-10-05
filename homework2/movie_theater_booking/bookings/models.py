from django.db import models
from django.conf import settings
import datetime

# Movie: title, description, release date, duration.
class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    release_date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")

    def __str__(self):
        return self.title


# Seat: seat number, booking status.
class Seat(models.Model):
    seat_number = models.CharField(max_length=10, unique=True)  # allow A10, B10, etc.
    is_booked = models.BooleanField(default=False)               # renamed for clarity

    def __str__(self):
        return self.seat_number


# Booking: movie, seat, user, booking date
class Booking(models.Model):
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="bookings"
    )
    seat = models.ForeignKey(
        Seat, on_delete=models.PROTECT, related_name="bookings"  # PROTECT recommended
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings"
    )
    booking_date = models.DateTimeField(auto_now_add=True)
    show_date = models.DateField()
    booking_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent double-booking the same seat for the same movie
        unique_together = ("movie", "seat")

    def __str__(self):
        return f"{self.user} -> {self.movie.title} {self.seat.seat_number} on {self.show_date}"
