from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ServiceCategory(TimeStampedModel):
    """A grouping for services, e.g. Makeup, Hair, Skin & Body, Nail Art."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    icon = models.ImageField(upload_to="categories/icons/", blank=True, null=True,
                              help_text="Small square icon representing the category (optional).")
    description = models.CharField(max_length=255, blank=True,
                                    help_text="One-line description shown under the category name.")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("studio:services") + f"?category={self.slug}"

    @property
    def active_services(self):
        return self.services.filter(is_active=True).order_by("order", "name")


class Service(TimeStampedModel):
    """An individual service, e.g. 'Bridal Makeup', 'Keratin Treatment'."""

    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name="services")
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    short_description = models.CharField(max_length=200, blank=True,
                                          help_text="Short teaser shown on cards/listing pages.")
    description = models.TextField(blank=True, help_text="Full description shown on the service detail page.")
    image = models.ImageField(upload_to="services/", blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2,
                                 help_text="Starting price in ₹. Use 0 if price is 'On Request'.")
    price_on_request = models.BooleanField(default=False,
                                            help_text="If checked, shows 'On Request' instead of the price.")
    duration_minutes = models.PositiveIntegerField(default=60, help_text="Approx. duration in minutes.")
    is_featured = models.BooleanField(default=False, help_text="Feature this service on the home page.")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Service.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("studio:service_detail", kwargs={"slug": self.slug})

    @property
    def display_price(self):
        if self.price_on_request or self.price == 0:
            return "On Request"
        return f"₹{self.price:,.0f}"

    @property
    def display_duration(self):
        hrs, mins = divmod(self.duration_minutes, 60)
        if hrs and mins:
            return f"{hrs} hr {mins} min"
        if hrs:
            return f"{hrs} hr"
        return f"{mins} min"


class GalleryCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Gallery Category"
        verbose_name_plural = "Gallery Categories"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class GalleryImage(TimeStampedModel):
    title = models.CharField(max_length=150, blank=True)
    category = models.ForeignKey(GalleryCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name="images")
    image = models.ImageField(upload_to="gallery/")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title or f"Gallery Image #{self.pk}"


class TeamMember(TimeStampedModel):
    name = models.CharField(max_length=150)
    designation = models.CharField(max_length=150, help_text="e.g. Founder & Lead Makeup Artist")
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="team/", blank=True, null=True)
    instagram_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Testimonial(TimeStampedModel):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    client_name = models.CharField(max_length=150)
    client_photo = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name="testimonials")
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5,
                                               validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.TextField()
    is_approved = models.BooleanField(default=False,
                                       help_text="Only approved testimonials are shown on the website.")
    is_featured = models.BooleanField(default=False, help_text="Show prominently on the home page.")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.client_name} ({self.rating} star)"

    @property
    def star_range(self):
        return range(self.rating)

    @property
    def empty_star_range(self):
        return range(5 - self.rating)


class Booking(TimeStampedModel):
    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name="bookings")
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    location_preference = models.CharField(
        max_length=20,
        choices=[("studio", "At the Studio"), ("home", "At Home / Venue")],
        default="studio",
    )
    notes = models.TextField(blank=True, help_text="Any special requests from the client.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    class Meta:
        ordering = ["-preferred_date", "-preferred_time"]

    def __str__(self):
        return f"{self.full_name} - {self.service} on {self.preferred_date}"


class ContactMessage(TimeStampedModel):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject or 'No subject'}"


class SiteSettings(models.Model):
    """Singleton model: all editable site-wide content lives here, editable from the admin
    without touching a single line of code."""

    site_name = models.CharField(max_length=150, default="Hunny's Makeover Studio")
    tagline = models.CharField(max_length=200, default="Where Every Look Tells a Story")
    logo = models.ImageField(upload_to="site/", blank=True, null=True)

    # Hero section
    hero_heading = models.CharField(max_length=200, default="Beauty, Tailored to You")
    hero_subheading = models.CharField(
        max_length=300,
        default="Bridal & party makeup, hairstyling and skin care in an elegant, private studio setting."
    )
    hero_image = models.ImageField(upload_to="site/", blank=True, null=True)

    # About section
    about_title = models.CharField(max_length=200, default="The Studio Story")
    about_text = models.TextField(
        default="Hunny's Makeover Studio was founded on a simple belief: every client deserves to feel like "
                "the most beautiful version of themselves. From intimate bridal mornings to glamorous party "
                "looks, our artists blend technique with heart to create looks that photograph beautifully "
                "and last all day."
    )
    about_image = models.ImageField(upload_to="site/", blank=True, null=True)
    years_experience = models.PositiveIntegerField(default=8)
    happy_clients = models.PositiveIntegerField(default=2500)
    services_offered = models.PositiveIntegerField(default=20)

    # Contact & socials
    phone = models.CharField(max_length=20, default="+91 90000 00000")
    whatsapp_number = models.CharField(max_length=20, default="919000000000",
                                        help_text="Digits only, with country code, no + or spaces (used in wa.me links).")
    email = models.EmailField(default="hello@hunnysmakeoverstudio.com")
    address = models.CharField(max_length=255, default="123 Rosewood Lane, Vadodara, Gujarat")
    google_maps_embed_url = models.URLField(blank=True, help_text="Paste a Google Maps embed URL.")
    opening_hours = models.CharField(max_length=255, default="Tue - Sun: 10:00 AM - 8:00 PM (Mon Closed)")
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    pinterest_url = models.URLField(blank=True)

    footer_note = models.CharField(max_length=255, default="Studio & at-home appointments available.")

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    def save(self, *args, **kwargs):
        self.pk = 1  # enforce singleton
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # prevent deletion

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def whatsapp_link(self):
        return f"https://wa.me/{self.whatsapp_number}"
