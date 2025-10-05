from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer

from datetime import date

# ---------- Shared pagination ----------
class SmallResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 200


# ---------- API (DRF) ----------

class MovieViewSet(viewsets.ModelViewSet):
    """
    CRUD for movies.
    Extras:
      - ?q=<text> search in title/description
    """
    serializer_class = MovieSerializer
    pagination_class = SmallResultsSetPagination

    def get_queryset(self):
        qs = Movie.objects.all().order_by('title')
        q = self.request.query_params.get('q')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        return qs


class SeatViewSet(viewsets.ModelViewSet):
    """
    CRUD for seats.
    Extras:
      - ?available=true to filter only unbooked seats
      - GET  /api/seats/available/   -> list unbooked seats
      - POST /api/seats/{id}/book/   -> book specific seat (body: {"user":<id>, "movie":<id>})
      - POST /api/seats/{id}/unbook/ -> free a seat (utility)
    """
    serializer_class = SeatSerializer
    pagination_class = SmallResultsSetPagination

    def get_queryset(self):
        qs = Seat.objects.all().order_by('seat_number')
        available = self.request.query_params.get('available')
        if available is not None:
            if str(available).lower() in {'1', 'true', 'yes', 'y', 'on'}:
                qs = qs.filter(is_booked=False)
        return qs

    @action(detail=False, methods=['get'])
    def available(self, request):
        qs = Seat.objects.filter(is_booked=False).order_by('seat_number')
        page = self.paginate_queryset(qs)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)
        ser = self.get_serializer(qs, many=True)
        return Response(ser.data)

    @action(detail=True, methods=['post'])
    def book(self, request, pk=None):
        """
        Concurrency-safe booking using a DB transaction.
        Body: {"user": <id>, "movie": <id>}
        """
        seat = self.get_object()
        user_id = request.data.get('user')
        movie_id = request.data.get('movie')
        show_date = request.data.get('show_date')

        with transaction.atomic():
            try:
                seat = Seat.objects.select_for_update().get(pk=pk)
            except Seat.DoesNotExist:
                return Response({'detail': 'Seat not found.'}, status=status.HTTP_404_NOT_FOUND)

            if seat.is_booked:
                return Response({'detail': 'Seat already booked.'}, status=status.HTTP_400_BAD_REQUEST)
            if not user_id or not movie_id:
                return Response({'detail': 'user and movie are required.'}, status=status.HTTP_400_BAD_REQUEST)
            if not show_date:
                return Response({'detail': 'show_date is required (YYYY-MM-DD).'}, status=status.HTTP_400_BAD_REQUEST)

            user = get_object_or_404(User, pk=user_id)
            movie = get_object_or_404(Movie, pk=movie_id)

            serializer = BookingSerializer(data={'seat': seat.id, 'movie': movie.id, 'user': user.id, 'show_date': show_date,})
            serializer.is_valid(raise_exception=True)
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def unbook(self, request, pk=None):
        """
        Utility to free a seat (deletes any associated booking).
        """
        with transaction.atomic():
            seat = get_object_or_404(Seat.objects.select_for_update(), pk=pk)
            if not seat.is_booked:
                return Response({'detail': 'Seat is not booked.'}, status=status.HTTP_400_BAD_REQUEST)
            Booking.objects.filter(seat=seat).delete()
            seat.is_booked = False
            seat.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookingViewSet(viewsets.ModelViewSet):
    """
    CRUD for bookings.
    Extras:
      - ?user=<id> or ?username=<name> to filter
      - GET  /api/bookings/mine/           -> bookings for current user or ?username=
      - POST /api/bookings/{id}/cancel/    -> cancel booking & free seat
    """
    serializer_class = BookingSerializer
    pagination_class = SmallResultsSetPagination

    def get_queryset(self):
        qs = (Booking.objects
              .select_related('movie', 'seat', 'user')
              .order_by('-booking_date'))
        user_id = self.request.query_params.get('user')
        username = self.request.query_params.get('username')
        if user_id:
            qs = qs.filter(user_id=user_id)
        if username:
            qs = qs.filter(user__username=username)
        return qs

    @action(detail=False, methods=['get'])
    def mine(self, request):
        if request.user.is_authenticated:
            qs = (Booking.objects.filter(user=request.user)
                  .select_related('movie', 'seat')
                  .order_by('-booking_date'))
        else:
            username = request.query_params.get('username')
            if not username:
                return Response({'detail': 'Provide ?username when not authenticated.'},
                                status=status.HTTP_400_BAD_REQUEST)
            qs = (Booking.objects.filter(user__username=username)
                  .select_related('movie', 'seat')
                  .order_by('-booking_date'))

        page = self.paginate_queryset(qs)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)
        ser = self.get_serializer(qs, many=True)
        return Response(ser.data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        with transaction.atomic():
            booking = get_object_or_404(Booking.objects.select_related('seat'), pk=pk)
            seat = booking.seat
            booking.delete()
            seat.is_booked = False
            seat.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------- HTML views (Templates) ----------

def movie_list_view(request):
    movies = Movie.objects.all().order_by('title')
    return render(request, 'bookings/movie_list.html', {'movies': movies})


def seat_booking_view(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    seats = Seat.objects.filter(is_booked=False).order_by('seat_number')
    # provide default date for the picker
    context = {'movie': movie, 'seats': seats, 'today': date.today().isoformat()}

    if request.method == 'POST':
        seat_id = request.POST.get('seat_id')
        show_date = request.POST.get('show_date')  
        if not show_date:
            context['error'] = 'Please pick a date.'
            return render(request, 'bookings/seat_booking.html', context)

        username = request.POST.get('username', 'demo')
        user, _ = User.objects.get_or_create(username=username)

        with transaction.atomic():
            seat = get_object_or_404(Seat.objects.select_for_update(), pk=seat_id)
            if seat.is_booked:
                context['error'] = 'That seat is already booked. Pick another.'
                return render(request, 'bookings/seat_booking.html', context)

            # PASS show_date into the Booking
            Booking.objects.create(movie=movie, seat=seat, user=user, show_date=show_date)
            seat.is_booked = True
            seat.save()

        return redirect('booking_history')

    return render(request, 'bookings/seat_booking.html', context)


def booking_history_view(request):
    bookings = Booking.objects.select_related('movie', 'seat', 'user').order_by('-booking_date')
    # Always return a response
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})