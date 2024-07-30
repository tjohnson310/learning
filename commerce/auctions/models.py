from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return self.username
    pass


class Listing(models.Model):
    listing_user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(decimal_places=2, max_digits=10)
    image_url = models.CharField(max_length=300)
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    bidding_user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    new_bid = models.DecimalField(decimal_places=2, max_digits=10)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.TextField()


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listings = models.ManyToManyField(Listing)

