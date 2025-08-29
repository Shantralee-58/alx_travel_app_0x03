from django.shortcuts import render
from rest_framework import viewsets
from .models import Listing, Booking, Review
from .serializers import ListingSerializer, BookingSerializer, ReviewSerializer
from django.shortcuts import get_object_or_404
import os
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Payment
from dotenv import load_dotenv
import uuid

load_dotenv()

CHAPA_SECRET_KEY = os.getenv('CHAPA_SECRET_KEY')
CHAPA_BASE_URL = os.getenv('CHAPA_BASE_URL', 'https://api.chapa.co/v1')


@csrf_exempt
def initiate_payment(request):
    """
    Initiates a payment with Chapa and returns checkout URL
    Expects JSON: { "user_id": int, "booking_reference": str, "amount": float, "email": str }
    """
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required"}, status=400)

    data = request.POST or request.body
    import json
    try:
        data = json.loads(data)
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    user_id = data.get("user_id")
    booking_reference = data.get("booking_reference")
    amount = data.get("amount")
    email = data.get("email")

    if not all([user_id, booking_reference, amount, email]):
        return JsonResponse({"error": "Missing required fields"}, status=400)

    # Create initial Payment record
    payment = Payment.objects.create(
        user_id=user_id,
        booking_reference=booking_reference,
        amount=amount,
        status='Pending'
    )

    # Generate unique transaction reference
    tx_ref = str(uuid.uuid4())
    
    payload = {
        "amount": str(amount),
        "currency": "ETB",
        "email": email,
        "first_name": "User",
        "last_name": "Booking",
        "tx_ref": tx_ref
    }

    headers = {
        "Authorization": f"Bearer {CHAPA_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(f"{CHAPA_BASE_URL}/transaction/initialize", json=payload, headers=headers)
        if response.status_code == 200:
            res_data = response.json()
            checkout_url = res_data['data']['checkout_url']
            payment.transaction_id = tx_ref
            payment.save()
            return JsonResponse({"checkout_url": checkout_url, "payment_id": payment.id})
        else:
            payment.status = 'Failed'
            payment.save()
            return JsonResponse({"error": response.json()}, status=response.status_code)
    except Exception as e:
        payment.status = 'Failed'
        payment.save()
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def verify_payment(request, payment_id):
    """
    Verify payment status with Chapa
    """
    try:
        payment = Payment.objects.get(id=payment_id)
    except Payment.DoesNotExist:
        return JsonResponse({"error": "Payment not found"}, status=404)

    if not payment.transaction_id:
        return JsonResponse({"error": "Transaction ID missing"}, status=400)

    try:
        response = requests.get(
            f"{CHAPA_BASE_URL}/transaction/verify/{payment.transaction_id}",
            headers={"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}
        )
        res_data = response.json()

        if res_data['status'] == 'success' and res_data['data']['status'] == 'success':
            payment.status = 'Completed'
            payment.save()
            # TODO: Trigger confirmation email via Celery
            return JsonResponse({"status": "Completed"})
        else:
            payment.status = 'Failed'
            payment.save()
            return JsonResponse({"status": "Failed"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

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
