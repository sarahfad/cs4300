# bookings/tests.py
#used chatgpt to start off the tests, and for the integration testing since I didn't know how to do those
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Movie, Seat, Booking


# Unit Tests
class ModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="alice")
        self.movie = Movie.objects.create(
            title="Wicked",
            description="Galinda and Elphaba go on an adventure",
            release_date=date(2024, 11, 22),
            duration=160,
        )
        self.seat = Seat.objects.create(seat_number="A1")

    def test_movie_str_and_fields(self):
        self.assertEqual(str(self.movie), "Wicked")
        self.assertEqual(self.movie.duration, 160)
        self.assertEqual(self.movie.release_date, date(2024, 11, 22))

    def test_seat_unique_number(self):
        with self.assertRaises(IntegrityError):
            Seat.objects.create(seat_number="A1") #should fail

    def test_booking_creation_with_show_date(self):
        show = timezone.localdate() + timedelta(days=1)
        b = Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            user=self.user,
            show_date=show,
        )
        self.assertIn(self.movie.title, str(b))
        self.assertEqual(b.show_date, show)

    def test_booking_requires_show_date(self):
        #  should fail if we try without show_date
        with self.assertRaises(IntegrityError):
            Booking.objects.create(
                movie=self.movie,
                seat=self.seat,
                user=self.user,
                # show_date gone = IntegrityError
            )


# Integration Tests
class ApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="bob")
        self.movie = Movie.objects.create(
            title="Wicked",
            description="Galinda and Elphaba go on adventures",
            release_date=date(2024, 11, 22),
            duration=160,
        )
    
        self.seat1 = Seat.objects.create(seat_number="A1")
        self.seat2 = Seat.objects.create(seat_number="A2")

    # ---- Movies endpoints ----
    def test_movies_list_get_200_and_shape(self):
        url = reverse("movie-list")           # /api/movies/
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(res.data, list) or "results" in res.data)  # paginated or not

    def test_movies_create_post_201(self):
        url = reverse("movie-list")
        payload = {
            "title": "Barbie",
            "description": "Barbie and Ken leave Barbieland.",
            "release_date": "2023-07-21",
            "duration": 114,
        }
        res = self.client.post(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["title"], "Barbie")

    # seats 
    def test_seats_list_and_available(self):
        url_all = reverse("seat-list")        # /api/seats/
        url_avail = reverse("seat-available") # /api/seats/available/
        self.assertEqual(self.client.get(url_all).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(url_avail).status_code, status.HTTP_200_OK)

    def test_book_seat_success_and_double_book_blocked(self):
        show = (timezone.localdate() + timedelta(days=2)).isoformat()
        book_url = reverse("seat-book", args=[self.seat1.id])   # /api/seats/{id}/book/

        # First booking succeeds
        res1 = self.client.post(book_url, {
            "user": self.user.id,
            "movie": self.movie.id,
            "show_date": show
        }, format="json")
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)

        # Seat should be marked booked
        self.seat1.refresh_from_db()
        self.assertTrue(self.seat1.is_booked)

        # Second booking on same seat should be blocked
        res2 = self.client.post(book_url, {
            "user": self.user.id,
            "movie": self.movie.id,
            "show_date": show
        }, format="json")
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Seat already booked", str(res2.data))

    # booking endpoints
    def test_bookings_list_and_mine_and_cancel(self):
        show = (timezone.localdate() + timedelta(days=3)).isoformat()

        # Create a booking through /api/bookings/
        create_url = reverse("booking-list")  # /api/bookings/
        res_create = self.client.post(create_url, {
            "user": self.user.id,
            "movie": self.movie.id,
            "seat": self.seat2.id,
            "show_date": show
        }, format="json")
        self.assertEqual(res_create.status_code, status.HTTP_201_CREATED)
        booking_id = res_create.data["id"]

        # /api/bookings/ should list it
        res_list = self.client.get(create_url)
        self.assertEqual(res_list.status_code, status.HTTP_200_OK)
        # paginated or not—normalize
        items = res_list.data if isinstance(res_list.data, list) else res_list.data.get("results", [])
        self.assertTrue(any(b.get("id") == booking_id for b in items))

        # /api/bookings/mine/?username=bob should include it
        mine_url = reverse("booking-mine")
        res_mine = self.client.get(mine_url, {"username": "bob"})
        self.assertEqual(res_mine.status_code, status.HTTP_200_OK)
        mine_items = res_mine.data if isinstance(res_mine.data, list) else res_mine.data.get("results", [])
        self.assertTrue(any(b.get("id") == booking_id for b in mine_items))

        # Cancel booking: /api/bookings/{id}/cancel/
        cancel_url = reverse("booking-cancel", args=[booking_id])
        res_cancel = self.client.post(cancel_url)
        self.assertEqual(res_cancel.status_code, status.HTTP_204_NO_CONTENT)

        # Seat freed
        self.seat2.refresh_from_db()
        self.assertFalse(self.seat2.is_booked)
