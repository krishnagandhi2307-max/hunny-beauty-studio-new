from django.urls import path
from . import views

app_name = "studio"

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("services/<slug:slug>/", views.service_detail, name="service_detail"),
    path("gallery/", views.gallery, name="gallery"),
    path("about/", views.about, name="about"),
    path("booking/", views.booking, name="booking"),
    path("booking/success/", views.booking_success, name="booking_success"),
    path("contact/", views.contact, name="contact"),
]
