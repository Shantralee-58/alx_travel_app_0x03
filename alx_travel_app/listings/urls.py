from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from .views import ListingViewset, BookingViewset

# class HelloView(APIView):
#     def get(self, request):
#         return Response({"message": "Hello, ALX Travel!"})

router = DefaultRouter()
router.register(r'listings', ListingViewset, basename='listing')
router.register(r'bookings', BookingViewset, basename='booking')  

urlpatterns = [
    path('api/', include(router.urls)),
]
# urlpatterns = [
#     # path('hello/', HelloView.as_view(), name='hello'),
#     path('api/', include(router.urls)),
# ]
