from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createNewListing", views.createListing, name="newListing"),
    path("create", views.createListing, name="create"),
    path("watchList", views.displayWatchList, name="watchList"),
    path("removedListing",views.removedListing,name="removedListing"),
    path("categories", views.categoriesList, name="categoriesList"),
    path("categories/<str:category>",
         views.displayAllCategories, name="displayCategory"),
    path("individualListing/placeBid",
         views.placeBid, name="placeBid"),
    path("individualListing/comment", views.makeComment, name="comment"),
    path("closeThisListing/<str:title>",
         views.closeThisListing, name="closeThisListing"),
    path("individualListing/<str:listingTitle>",
         views.individualListing, name="individualListing"),
    path("individualListing/addToWatchList/<str:title>",
         views.addToWatchList, name="addToWatchList"),
    path("individualListing/removeFromWatchList/<str:title>",
         views.removeFromWatchList, name="removeFromWatchList"),
    path("individualListing/<str:listingTitle>/<str:checkBid>",
         views.individualListing, name="individualListingBid"),
]
