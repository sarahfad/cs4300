from rest_framework import serializers
from .models import Movie, Seat, Booking

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('booking_date',)

    def validate(self, attrs):
        seat = attrs.get('seat')
        if seat.is_booked:
            raise serializers.ValidationError({'seat': 'This seat is already booked.'})
        if not attrs.get('show_date'):
            raise serializers.ValidationError({'show_date': 'This field is required.'})
        return attrs

    def create(self, validated_data):
        # mark seat as booked atomically
        seat = validated_data['seat']
        seat.is_booked = True
        seat.save()
        return super().create(validated_data)
