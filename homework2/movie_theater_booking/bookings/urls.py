from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MovieViewSet, SeatViewSet, BookingViewSet,
    movie_list_view, seat_booking_view, booking_history_view
)

router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'seats', SeatViewSet, basename='seat')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    # HTML pages
    path('', movie_list_view, name='movie_list'),
    path('book/<int:movie_id>/', seat_booking_view, name='book_seat'),
    path('history/', booking_history_view, name='booking_history'),

    # API
    path('api/', include(router.urls)),
]
