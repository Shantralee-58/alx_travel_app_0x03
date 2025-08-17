from django.shortcuts import render
from rest_framework import viewsets
from .models import Listing, Booking, Review
from .serializers import ListingSerializer, BookingSerializer, ReviewSerializer
from django.shortcuts import get_object_or_404
# Create your views here.

class ListingViewset(viewsets.ModelViewSet):
    serializer_class = [ListingSerializer]
    queryset = Booking.objects.all()

    def perform_create(self, serializer):
        listing = serializer.save()
        listing.user.add(self.request.user)

class BookingViewset(viewsets.ModelViewSet):
    serializer_class = [BookingSerializer]

    def perform_create(self, serializer):
        listing_id = self.request.data.get('listing_id')
        listing = get_object_or_404(Listing, id=listing_id)

        serializer.save(user=self.request.user, listing=listing)
