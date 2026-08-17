from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import (
    ServiceCategory, Service, GalleryCategory, GalleryImage,
    TeamMember, Testimonial, SiteSettings,
)
from .forms import BookingForm, ContactForm


def home(request):
    settings_obj = SiteSettings.load()
    featured_services = Service.objects.filter(is_active=True, is_featured=True).select_related("category")[:8]
    if featured_services.count() < 4:
        featured_services = Service.objects.filter(is_active=True).select_related("category")[:8]
    main_category_names = [
        "Makeup Services",
        "Hairstyling",
        "Nail Extensions & Art",
        "Bridal Packages",
    ]
    categories = ServiceCategory.objects.filter(
        is_active=True,
        name__in=main_category_names,
    ).order_by("order", "name")
    gallery_preview = GalleryImage.objects.filter(is_active=True)[:8]
    testimonials = Testimonial.objects.filter(is_approved=True).order_by("-is_featured", "-created_at")[:6]
    team = TeamMember.objects.filter(is_active=True).order_by("order")[:4]

    context = {
        "settings": settings_obj,
        "featured_services": featured_services,
        "categories": categories,
        "gallery_preview": gallery_preview,
        "testimonials": testimonials,
        "team": team,
    }
    return render(request, "studio/home.html", context)


def services(request):
    category_slug = request.GET.get("category")
    services_qs = Service.objects.filter(is_active=True).select_related("category").order_by(
        "category__order", "order", "name"
    )
    categories = ServiceCategory.objects.filter(is_active=True).order_by("order", "name")
    active_category = None

    if category_slug:
        active_category = get_object_or_404(ServiceCategory, slug=category_slug, is_active=True)
        services_qs = services_qs.filter(category=active_category)

    search_query = request.GET.get("q", "").strip()
    if search_query:
        services_qs = services_qs.filter(
            Q(name__icontains=search_query) | Q(short_description__icontains=search_query)
        )

    context = {
        "services": services_qs,
        "categories": categories,
        "active_category": active_category,
        "search_query": search_query,
    }
    return render(request, "studio/services.html", context)


def service_detail(request, slug):
    service = get_object_or_404(Service.objects.select_related("category"), slug=slug, is_active=True)
    related_services = Service.objects.filter(
        category=service.category, is_active=True
    ).exclude(pk=service.pk)[:4]
    testimonials = Testimonial.objects.filter(is_approved=True, service=service)[:5]
    context = {
        "service": service,
        "related_services": related_services,
        "testimonials": testimonials,
    }
    return render(request, "studio/service_detail.html", context)


def gallery(request):
    category_slug = request.GET.get("category")
    images_qs = GalleryImage.objects.filter(is_active=True).select_related("category")
    categories = GalleryCategory.objects.all()
    active_category = None

    if category_slug:
        active_category = get_object_or_404(GalleryCategory, slug=category_slug)
        images_qs = images_qs.filter(category=active_category)

    paginator = Paginator(images_qs, 16)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "categories": categories,
        "active_category": active_category,
    }
    return render(request, "studio/gallery.html", context)


def about(request):
    team = TeamMember.objects.filter(is_active=True).order_by("order")
    testimonials = Testimonial.objects.filter(is_approved=True).order_by("-is_featured", "-created_at")[:6]
    context = {"team": team, "testimonials": testimonials}
    return render(request, "studio/about.html", context)


def booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            new_booking = form.save()
            messages.success(
                request,
                "Thank you! Your appointment request has been received. "
                "Our team will call you shortly to confirm the details."
            )
            return redirect("studio:booking_success")
    else:
        initial = {}
        service_slug = request.GET.get("service")
        if service_slug:
            svc = Service.objects.filter(slug=service_slug, is_active=True).first()
            if svc:
                initial["service"] = svc.pk
        form = BookingForm(initial=initial)

    context = {"form": form}
    return render(request, "studio/booking.html", context)


def booking_success(request):
    return render(request, "studio/booking_success.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent. We'll get back to you soon!")
            return redirect("studio:contact")
    else:
        form = ContactForm()

    context = {"form": form}
    return render(request, "studio/contact.html", context)