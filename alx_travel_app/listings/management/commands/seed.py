from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing, Booking
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Seed the database with test data'

    def handle(self, *args, **kwargs):
        # Create Users
        for i in range(1, 4):
            username = f"user{i}"
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, password="pass1234")
        users = User.objects.all()

        # Create Listings
        for i in range(5):
            Listing.objects.create(
                title=f"Listing {i+1}",
                description="Beautiful place.",
                price_per_night=random.randint(100, 300),
                location=f"City {i+1}",
                owner=random.choice(users)
            )

        listings = Listing.objects.all()

        # Create Bookings
        for listing in listings:
            Booking.objects.create(
                listing=listing,
                user=random.choice(users),
                start_date=datetime.today().date(),
                end_date=datetime.today().date() + timedelta(days=random.randint(1, 5))
            )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully! 🎉'))

