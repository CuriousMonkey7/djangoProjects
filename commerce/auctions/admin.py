from django.contrib import admin

# Register your models here.
from .models import AuctionListing, User, Bids, Comment, WishList
admin.site.register(AuctionListing)
admin.site.register(User)
admin.site.register(Bids)
admin.site.register(Comment)

admin.site.register(WishList)
