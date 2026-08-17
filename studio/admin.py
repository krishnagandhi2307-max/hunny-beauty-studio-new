from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ServiceCategory, Service, GalleryCategory, GalleryImage,
    TeamMember, Testimonial, Booking, ContactMessage, SiteSettings,
)


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "is_active", "service_count")
    list_editable = ("order", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)

    def service_count(self, obj):
        return obj.services.count()
    service_count.short_description = "Services"


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 0
    fields = ("name", "price", "is_featured", "is_active", "order")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "display_price", "duration_minutes", "is_featured", "is_active", "order", "thumb")
    list_editable = ("is_featured", "is_active", "order")
    list_filter = ("category", "is_featured", "is_active")
    search_fields = ("name", "short_description", "description")
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        ("Basic Info", {"fields": ("category", "name", "slug", "short_description", "description", "image")}),
        ("Pricing & Duration", {"fields": ("price", "price_on_request", "duration_minutes")}),
        ("Visibility", {"fields": ("is_featured", "is_active", "order")}),
    )

    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:6px;" />', obj.image.url)
        return "-"
    thumb.short_description = "Image"


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_active", "order", "thumb")
    list_editable = ("is_active", "order")
    list_filter = ("category", "is_active")

    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:6px;" />', obj.image.url)
        return "-"
    thumb.short_description = "Preview"


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "designation", "is_active", "order", "thumb")
    list_editable = ("is_active", "order")

    def thumb(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height:40px;border-radius:50%;" />', obj.photo.url)
        return "-"
    thumb.short_description = "Photo"


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("client_name", "rating", "service", "is_approved", "is_featured", "created_at")
    list_editable = ("is_approved", "is_featured")
    list_filter = ("is_approved", "is_featured", "rating")
    search_fields = ("client_name", "review_text")
    actions = ["approve_testimonials"]

    def approve_testimonials(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} testimonial(s) approved.")
    approve_testimonials.short_description = "Approve selected testimonials"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "service", "preferred_date", "preferred_time",
                    "location_preference", "status", "created_at")
    list_editable = ("status",)
    list_filter = ("status", "location_preference", "preferred_date", "service")
    search_fields = ("full_name", "phone", "email")
    date_hierarchy = "preferred_date"
    actions = ["mark_confirmed", "mark_completed", "mark_cancelled"]

    def mark_confirmed(self, request, queryset):
        queryset.update(status=Booking.STATUS_CONFIRMED)
    mark_confirmed.short_description = "Mark selected as Confirmed"

    def mark_completed(self, request, queryset):
        queryset.update(status=Booking.STATUS_COMPLETED)
    mark_completed.short_description = "Mark selected as Completed"

    def mark_cancelled(self, request, queryset):
        queryset.update(status=Booking.STATUS_CANCELLED)
    mark_cancelled.short_description = "Mark selected as Cancelled"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "subject", "is_read", "created_at")
    list_editable = ("is_read",)
    list_filter = ("is_read",)
    search_fields = ("name", "email", "message")


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Branding", {"fields": ("site_name", "tagline", "logo")}),
        ("Hero Section", {"fields": ("hero_heading", "hero_subheading", "hero_image")}),
        ("About Section", {"fields": ("about_title", "about_text", "about_image",
                                       "years_experience", "happy_clients", "services_offered")}),
        ("Contact Details", {"fields": ("phone", "whatsapp_number", "email", "address",
                                         "opening_hours", "google_maps_embed_url")}),
        ("Social Links", {"fields": ("instagram_url", "facebook_url", "youtube_url", "pinterest_url")}),
        ("Footer", {"fields": ("footer_note",)}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.site_header = "Hunny's Makeover Studio — Admin"
admin.site.site_title = "Hunny's Makeover Studio"
admin.site.index_title = "Manage your website content"
