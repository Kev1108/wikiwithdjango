from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="title"),
    path("search/", views.search, name="search"),
    path("create/", views.to_create_page, name="to_create"),
    path("addpage/", views.create_page, name="create"),
    path("edit/<str:title>", views.to_edit_page, name="to_edit"),
    path("editpage/", views.edit_page, name= "edit" ),
    path("random/", views.random_page, name="random")
]
