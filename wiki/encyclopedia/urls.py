from django.urls import path

from . import views

urlpatterns = [

    path("", views.index, name="index"),
    path(
        "search", views.search, name="search"),

    path("createNewPage", views.createNewPage, name="newPage"),
    path("create", views.create, name="CreateNewEntry"),
    path("random", views.randomPage, name="random"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("editPage/<str:title>", views.editPage, name="editPage"),
    path("<str:title>", views.entry, name="entries"),
]
