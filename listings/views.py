from rest_framework import viewsets
from .models import Booking
from .serializers import BookingSerializer
from .tasks import send_booking_confirmation

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save()
        # Trigger Celery task asynchronously
        send_booking_confirmation.delay(
            booking.user.email,
            f"Booking ID: {booking.id}, Destination: {booking.destination}"
        )

