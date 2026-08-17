from .models import SiteSettings, ServiceCategory


def site_context(request):
    """Makes site-wide settings and the nav category list available in every template."""
    return {
        "site_settings": SiteSettings.load(),
        "nav_categories": ServiceCategory.objects.filter(is_active=True).order_by("order", "name"),
    }
