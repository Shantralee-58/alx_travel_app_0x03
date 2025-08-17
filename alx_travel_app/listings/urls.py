from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewset, BookingViewset, initiate_payment, verify_payment

# Create router and register viewsets
router = DefaultRouter()
router.register(r'listings', ListingViewset, basename='listing')
router.register(r'bookings', BookingViewset, basename='booking')

# URL patterns
urlpatterns = [
    # API routes for Listings and Bookings
    path('api/', include(router.urls)),

    # API routes for Payment
    path('api/payment/initiate/', initiate_payment, name='initiate_payment'),
    path('api/payment/verify/<int:payment_id>/', verify_payment, name='verify_payment'),
]

