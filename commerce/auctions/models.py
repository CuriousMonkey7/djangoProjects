from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    pass


class AuctionListing(models.Model):
    title = models.CharField(max_length=50, unique=True)
    category = models.TextField(blank=True, null=True)
    description = models.CharField(max_length=250)
    startingBid = models.IntegerField()
    currentPrice = models.IntegerField()
    imgUrl = models.URLField(max_length=200, blank=True, null=True)
    listBy = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="myListing")
    status = models.BooleanField(default="True")
    winner = models.ForeignKey(
        "User", null=True, blank=True, on_delete=models.CASCADE, related_name="MyWinning")

    def __str__(self):
        return self.title


class Bids(models.Model):

    item = models.ForeignKey(
        "AuctionListing", on_delete=models.CASCADE, related_name="bid")
    bidAmount = models.IntegerField()
    bidBy = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="myBid")

    def __str__(self):
        return str(self.bidAmount)+" by "+self.bidBy.username+" on "+self.item.title


class Comment(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="myComments")
    comment = models.TextField()
    commentedOn = models.ForeignKey(
        "AuctionListing", on_delete=models.CASCADE, related_name="commentsOnMe")

    def __str__(self):
        return f"comment by {self.user.username} on {self.commentedOn.title}"

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class WishList(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="wishlist")
    items = models.ForeignKey(
        "AuctionListing", on_delete=models.CASCADE, related_name="wishList")

    def __str__(self):
        return self.items.title

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'WishList'
        verbose_name_plural = 'WishLists'
