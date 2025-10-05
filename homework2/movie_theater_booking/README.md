# Movie Theater Booking App

A Django and REST framework web application for managing movies, seats and bookings - with HTML templates and API endpoints
This project uses a full-stack web development using Django, DRF, Bootstrap, and PostgreSQL (for deployment on Render)

Features: 
**Movies:** Browse and manage a list of available movies
**Booking History:** Browse booking history for movies
**REST API:** Expose endpoints for Movies, Seats, and Bookings
**Admin Panel:** Add or edit movies and seats (have to create a superuser for this - not necessary. You can just use the API endpoints)


## Local Setup

### 1. Clone the Repository
``` bash
git clone https://github.com/sarahfad/cs4300.git
cd cs4300/homework2/movie_theater_booking
```

### 2. Create a virtual enviornment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependancies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the server
```bash 
python manage.py runserver 0.0.0.0:3000
```

### 6. Vist the site
Paste: http://127.0.0.1:3000 into your local browser to view the site.


## Render (status = deployed)

If you want to visit the Render deployed site paste this link into your browser: https://movie-theater-booking-00zq.onrender.com/
(Might take a bit of time on the first startup)

You can also view the API endpoints by going to these links
https://movie-theater-booking-00zq.onrender.com/api/bookings/

^ Where you can book a movie and a seat for that movie

https://movie-theater-booking-00zq.onrender.com/api/movies/

^ Where you can view existing movies and add new ones

https://movie-theater-booking-00zq.onrender.com/api/seats/

^ Where you can add seats and view if they're booked or not



## Testing

To run automated tests navigate to homework2/movie_theater_booking

```bash
python manage.py test
```

## AI-Use

AI assistance (ChatGPT) was used to:
 - Debug and resolve Django and Render errors
 - Enhance front-end HTML/CSS
 - Help with the Unit tests and Integration testing