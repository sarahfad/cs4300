from django.contrib import admin
from .models import Movie, Seat, Booking

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'duration')
    search_fields = ('title',)

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'is_booked')
    list_filter = ('is_booked',)
    search_fields = ('seat_number',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'seat', 'booking_date')
    list_filter = ('movie', 'booking_date')
    search_fields = ('user__username', 'movie__title', 'seat__seat_number')
