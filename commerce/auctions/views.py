from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListing, WishList, Bids, Comment


def index(request):
    activeListing = []
    allListing = AuctionListing.objects.all()
    categoriesDic = {}
    for listing in allListing:
        if listing.status:
            categoriesDic[listing.title] = listing.category.split(",")
            activeListing.append(listing)

    return render(request, "auctions/index.html", {"listings": activeListing, "categories": categoriesDic})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def createListing(request):
    if request.method == 'POST' and request.user.is_authenticated:
        user = request.user
        title = request.POST["title"].strip().title()
        description = request.POST["description"]
        startingBid = request.POST["startingBid"]

        try:
            imgUrl = request.POST['imgUrl']
        except:
            imgUrl = None
        try:
            category = request.POST['category']
        except:
            category = "Not Listed in Any Category"
            pass
        try:
            titleCheck = AuctionListing.objects.get(title=title)
        except:
            titleCheck = False
        if not titleCheck:
            AuctionListing.objects.create(listBy=user, title=title,
                                          description=description,
                                          startingBid=startingBid, currentPrice=startingBid,
                                          imgUrl=imgUrl,
                                          category=category,)

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/createListing.html", {"errorMessage": "Title Already Exist"})

    else:
        return render(request, "auctions/createListing.html", {"signInError": "You Should SignIn To Create New Listing"})


def individualListing(request, listingTitle, checkBid="True"):

    listing = AuctionListing.objects.get(title=listingTitle.title())
    if listing.status:
        categories = listing.category.split(",")

        listedOnWatchList = False
        if request.user == listing.listBy:
            userIsOwner = True
        else:
            userIsOwner = False
        if request.user.is_authenticated:
            if (request.user.wishlist.filter(items=listing)):
                listedOnWatchList = True
        if (checkBid == "False"):
            checkBid = False
        else:
            CheckBid = True
        comments = listing.commentsOnMe.all()
        return render(request, "auctions/individualListing.html", {"listing": listing, "listedOnWatchList": listedOnWatchList, "checkBid": checkBid, "userIsOwner": userIsOwner, "comments": comments, "categories": categories})
    else:
        if request.user == listing.winner:
            return render(request, "auctions/notListed.html", {"winner": True})
        else:
            return render(request, "auctions/notListed.html",)


def addToWatchList(request, title):
    user = request.user
    listing = AuctionListing.objects.get(title=title.title())
    WishList.objects.create(user=user, items=listing)
    return HttpResponseRedirect(reverse("individualListing", args=[title]))


def removeFromWatchList(request, title):
    user = request.user
    listing = AuctionListing.objects.get(title=title.title())
    WishList.objects.filter(user=user, items=listing).delete()
    return HttpResponseRedirect(reverse("individualListing", args=[title]))


def placeBid(request):
    if request.method == "POST":

        title = request.POST["title"]
        bidAmount = int(request.POST["bidAmount"])
        listing = AuctionListing.objects.get(title=title)
        user = request.user
        if bidAmount > listing.currentPrice:
            listing.currentPrice = bidAmount
            listing.save()
            Bids.objects.create(bidBy=user, item=listing, bidAmount=bidAmount,)
            return HttpResponseRedirect(reverse("individualListing", args=[title]))
        elif bidAmount == listing.currentPrice and listing. currentPrice == listing.startingBid:
            listing.currentPrice = bidAmount
            listing.save()
            Bids.objects.create(bidBy=user, item=listing, bidAmount=bidAmount,)
            return HttpResponseRedirect(reverse("individualListing", args=[title]))
        else:
            return HttpResponseRedirect(reverse("individualListingBid", args=[title, "False"]))


def closeThisListing(request, title):
    listing = AuctionListing.objects.get(title=title.title())
    listing.status = False
    try:
        listing.winner = Bids.objects.get(bidAmount=listing.currentPrice).bidBy
    except:
        pass
    listing.save()
    return HttpResponseRedirect(reverse("individualListing", args=[title]))


def makeComment(request):
    if request.method == "POST":
        user = request.user
        comment = request.POST["comment"]
        title = request.POST["title"]
        listing = AuctionListing.objects.get(title=title)
        Comment.objects.create(user=user, comment=comment, commentedOn=listing)
        return HttpResponseRedirect(reverse("individualListing", args=[title]))


def displayWatchList(request):
    user = request.user
    watchList = user.wishlist.all()
    activeListing = []

    categoriesDic = {}
    for listing in watchList:
        if listing.items.status:
            categoriesDic[listing.items.title] = listing.items.category.split(
                ",")
            activeListing.append(listing)
    return render(request, "auctions/watchList.html", {"listings": activeListing, "categories": categoriesDic})


def categoriesList(request):
    categoriesList = []
    allListing = AuctionListing.objects.all()
    for listing in allListing:
        if listing.status:
            categoryInList = listing.category.split(",")
            for category in categoryInList:
                if not (category in categoriesList):

                    categoriesList.append(category.strip())

    return render(request, "auctions/categoriesList.html", {"categoriesList": categoriesList})


def displayAllCategories(request, category):

    listingAccToCategory = []
    allListing = AuctionListing.objects.all()
    categoriesDic = {}
    for listing in allListing:
        if listing.status:
            categories = listing.category.split(",")
            for categoryOfItem in categories:
                if categoryOfItem == category:
                    categoriesDic[listing.title] = categories
                    listingAccToCategory.append(listing)
    return render(request, "auctions/displayCategories.html", {"listings": listingAccToCategory, "category": category, "categories": categoriesDic})


def removedListing(request):
    removedListing = AuctionListing.objects.filter(status="False")
    categoriesDic = {}
    for listing in removedListing:
        categoriesDic[listing.title] = listing.category.split(
            ",")

    return render(request, "auctions/removedListing.html", {"listings": removedListing, "categories": categoriesDic})

    return render(request, "auctions/removedListing.html", {"listings": removedListing})
