from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings as dj_settings
from studio.models import ServiceCategory, Service, SiteSettings
import os


CATEGORY_DATA = [
    {"name": "Makeup Services", "description": "Everyday, party, HD and bridal makeup services.", "services": [
        ("Simple Base Makeup", 500, 45, True, "Simple base makeup — ₹500."),
        ("Party Makeup", 700, 60, True, "Party makeup — ₹700."),
        ("HD Makeup", 800, 75, True, "HD makeup — ₹800."),
        ("MAC Makeup", 700, 60, True, "Makeup using MAC products — ₹700."),
        ("Huda Beauty Makeup", 2500, 90, True, "Makeup using Huda Beauty products — ₹2,500."),
        ("Bridal Makeup", 5000, 150, True, "Bridal makeup — ₹5,000 onwards."),
    ]},
    {"name": "Bridal Packages", "description": "Complete bridal packages with makeup, hairstyling, draping and beauty-care inclusions.", "services": [
            ("Bridal Basic", 7000, 180, True, "1 facial and body treatment; 1 bridal makeup with jewellery; bridal hairstyle; draping."),
            ("Bridal Classic", 9000, 210, True, "1 facial and body treatment; 2 makeup looks with jewellery; hairstyling; draping."),
            ("Bridal Premium", 12000, 240, True, "1 facial and body treatment; hand nails; 2 makeup looks with jewellery; hairstyling; draping."),
            ("Bridal Deluxe", 15000, 270, True, "1 facial and body treatment; hand and foot nails; 3 makeup looks with jewellery; hairstyling; draping."),
            ("Bridal Luxury", 20000, 300, True, "2 facial and body treatments; hand and foot nails; full body wax; 4 makeup looks with jewellery; hairstyling; draping."),
        ]},{"name": "Regular Makeup Packages", "description": "Our most-booked complete makeup packages for local functions and special occasions.", "services": [
        ("Simple Makeup Package", 1000, 60, True, "₹1,000–₹1,200. Normal base, soft eye makeup and lips, simple hairstyle and normal draping."),
        ("Classic Makeup Package", 1500, 75, True, "₹1,500–₹1,800. HD base, shimmer eyes, chic updo, eyelashes, lenses and draping."),
        ("Signature Makeup Package", 2000, 90, True, "₹2,000–₹2,500. Waterproof HD base, detailed eyes, glam updo, eyelashes, lenses and draping."),
    ]},
    {"name": "Makeup Add-ons", "description": "Finishing touches available with a makeup service.", "services": [
        ("Contact Lens", 150, 10, False, "Contact lens add-on — ₹150."),
        ("False Lashes", 100, 10, False, "False lashes add-on — ₹100."),
        ("Makeup Draping", 100, 15, False, "Saree or dupatta draping with makeup — ₹100."),
    ]},
    {"name": "Hairstyling", "description": "Hairstyles for everyday looks, parties and bridal occasions.", "services": [
        ("Basic Hairstyle", 500, 30, False, "Basic hairstyle — ₹500 onwards."),
        ("Open Hairstyle", 500, 30, False, "Open hairstyle — ₹500 onwards."),
        ("Curls / Waves", 500, 40, True, "Curls or waves — ₹500 onwards."),
        ("Straight Hairstyle - Short Hair", 500, 35, False, "Straight hairstyle for short hair — ₹500 onwards."),
        ("Party Hairstyle", 700, 45, True, "Party hairstyle — ₹700 onwards."),
        ("Chic Updo", 800, 50, False, "Chic updo — ₹800 onwards."),
        ("Glam Updo", 900, 60, True, "Glam updo — ₹900 onwards."),
        ("Bridal Hairstyle", 1000, 75, True, "Bridal hairstyle — ₹1,000 onwards."),
        ("Hair Accessories Setting", 150, 15, False, "Hair accessories setting — ₹150 onwards."),
        ("Hair Extensions Setting", 500, 30, False, "Hair extensions setting — ₹500–₹700."),
    ]},
    {"name": "Hair Cutting", "description": "Precision cuts, trims and wash services for all ages.", "services": [
        ("One Length Cut", 200, 30, False, "One length haircut — ₹200."),
        ("U Cut / V Cut", 250, 35, False, "U cut or V cut — ₹250."),
        ("Layer Cut", 300, 45, True, "Layer haircut — ₹300."),
        ("Step Cut", 300, 45, False, "Step haircut — ₹300."),
        ("Butterfly Cut", 350, 50, True, "Butterfly haircut — ₹350."),
        ("Bob Cut", 300, 40, False, "Bob haircut — ₹300."),
        ("Curtain Bangs", 150, 20, False, "Curtain bangs — ₹150."),
        ("Front / Bangs Trim", 100, 15, False, "Front or bangs trim — ₹100."),
        ("Kids Haircut", 200, 30, False, "Kids haircut — ₹200."),
        ("Hair Wash + Blow Dry", 200, 35, False, "Hair wash with blow dry — ₹200."),
    ]},
    {"name": "Hair Treatments", "description": "Conditioning, repair and smoothing treatments; final price varies by hair length and density.", "services": [
        ("Hair Spa", 500, 60, True, "Deep conditioning and nourishing hair spa — ₹500."),
        ("Premium Hair Spa", 1000, 75, True, "Premium hair spa — ₹1,000."),
        ("Keratin Treatment", 2000, 120, False, "Keratin treatment — ₹2,000 onwards."),
        ("Hair Botox", 3000, 150, True, "Hair Botox treatment — ₹3,000 onwards."),
        ("Hair Smoothening", 3500, 180, False, "Hair smoothening — ₹3,500 onwards."),
        ("Nanoplastia", 3500, 180, True, "Nanoplastia treatment — ₹3,500 onwards."),
    ]},
    {"name": "Hair Colour", "description": "Professional colour services; final price varies by hair length, density and product quantity.", "services": [
        ("Basic Grey Root Coverage", 600, 60, False, "Grey root coverage — ₹600–₹1,000."),
        ("Premium Hair Colour", 1200, 90, True, "₹1,200–₹2,200+. Using L’Oréal Professionnel, Schwarzkopf or Wella."),
        ("Global Hair Colour", 2500, 120, True, "Global hair colour — ₹2,500 onwards."),
        ("Highlights + Colour", 4000, 180, True, "Highlights with hair colour — ₹4,000 onwards."),
    ]},
    {"name": "Gel Polish", "description": "Long-lasting gel polish for natural nails.", "services": [
        ("Gel Polish - Two Hands", 350, 45, False, "Gel polish for two hands — ₹350."),
        ("Gel Polish - Two Hands with Art", 400, 60, True, "Gel polish for two hands with nail art — ₹400."),
    ]},
    {"name": "Nail Extensions & Art", "description": "Nail extensions and detailed art finishes.", "services": [
        ("Basic Nail Extension + Basic Nail Art", 500, 75, False, "Basic nail extension with basic nail art — ₹500 onwards."),
        ("French Nail Extension", 550, 75, False, "French nail extension — ₹550 onwards."),
        ("Cat Eye Nail Extension", 600, 80, False, "Cat eye nail extension — ₹600 onwards."),
        ("Cat Eye + Nail Art Extension", 700, 90, True, "Cat eye extension with nail art — ₹700 onwards."),
        ("Chrome Nail Extension", 650, 80, False, "Chrome nail extension — ₹650 onwards."),
        ("Chrome + Cat Eye Extension", 800, 90, True, "Chrome and cat eye extension — ₹800 onwards."),
        ("Custom Nail Extension + Nail Art", 700, 100, True, "Custom nail extension with nail art — ₹700 onwards."),
        ("Cuticle Gel Extension", 800, 90, False, "Cuticle gel extension — ₹800 onwards."),
    ]},
    {"name": "Nail Removal", "description": "Safe removal of nail extensions and gel polish.", "services": [
        ("Nail Extension Removal", 200, 30, False, "Nail extension removal — ₹200."),
        ("Gel Polish Removal", 150, 20, False, "Gel polish removal — ₹150."),
    ]},
    {"name": "Press-On Nails", "description": "Ready-to-wear and custom reusable press-on nail sets.", "services": [
        ("Simple Press-On Nails", 400, 30, False, "Simple press-on nails — ₹400."),
        ("Press-On Nails with Art", 550, 45, True, "Press-on nails with art — ₹550."),
        ("Custom Press-On Nails", 600, 60, True, "Custom press-on nails — ₹600 onwards."),
        ("Press-On Nails Prep Kit", 100, 10, False, "Press-on nails preparation kit — ₹100."),
    ]},
    {"name": "Facial & Skin Care", "description": "Cleansing and glow treatments for refreshed, healthy-looking skin.", "services": [
        ("Basic Cleanup", 250, 35, False, "Cleansing, scrubbing, massage and face pack — ₹250."),
        ("Fruit Facial", 400, 50, False, "Fruit facial — ₹400."),
        ("Glow Facial", 500, 55, True, "Glow facial — ₹500."),
        ("De-Tan Facial", 550, 60, False, "De-tan facial — ₹550."),
        ("Gold Facial", 650, 60, True, "Gold facial — ₹650."),
        ("Bridal Glow Facial", 800, 75, True, "Bridal glow facial — ₹800."),
        ("Premium Facial", 1000, 90, True, "Premium facial — ₹1,000 onwards."),
    ]},
    {"name": "Facial Add-ons", "description": "Quick skin-care add-ons for a customised facial.", "services": [
        ("De-Tan Pack", 150, 20, False, "De-tan pack — ₹150."),
        ("Face Massage", 150, 20, False, "Face massage — ₹150."),
        ("Special Face Pack", 100, 20, False, "Special face pack — ₹100."),
    ]},
    {"name": "Normal Wax", "description": "Essential waxing services using normal wax.", "services": [
        ("Normal Wax - Full Arms", 150, 30, False, "Full arms with normal wax — ₹150."),
        ("Normal Wax - Half Arms", 100, 20, False, "Half arms with normal wax — ₹100."),
        ("Normal Wax - Full Legs", 200, 40, False, "Full legs with normal wax — ₹200."),
        ("Normal Wax - Half Legs", 150, 25, False, "Half legs with normal wax — ₹150."),
        ("Normal Wax - Underarms", 70, 10, False, "Underarms with normal wax — ₹70."),
        ("Normal Wax - Back", 250, 30, False, "Back with normal wax — ₹250."),
        ("Normal Wax - Stomach", 200, 25, False, "Stomach with normal wax — ₹200."),
        ("Normal Wax - Full Body", 700, 90, True, "Full body normal wax — ₹700 onwards."),
    ]},
    {"name": "Rica / Premium Wax", "description": "Gentler premium waxing services; final price varies by wax type and requirements.", "services": [
        ("Premium Wax - Full Arms", 250, 30, False, "Full arms with Rica or premium wax — ₹250."),
        ("Premium Wax - Full Legs", 300, 40, False, "Full legs with Rica or premium wax — ₹300."),
        ("Premium Wax - Underarms", 150, 15, False, "Underarms with Rica or premium wax — ₹150."),
        ("Premium Wax - Full Body", 1000, 100, True, "Full body Rica or premium wax — ₹1,000 onwards."),
    ]},
    {"name": "Threading & Eyebrows", "description": "Precise facial threading and eyebrow shaping.", "services": [
        ("Eyebrows", 30, 10, False, "Eyebrow threading — ₹30."),
        ("Upper Lips", 20, 10, False, "Upper-lip threading — ₹20."),
        ("Forehead Threading", 20, 10, False, "Forehead threading — ₹20."),
        ("Chin Threading", 30, 10, False, "Chin threading — ₹30."),
        ("Full Face Threading", 150, 30, True, "Full face threading — ₹150."),
    ]},
    {"name": "Threading Combos", "description": "Popular threading combinations at convenient package prices.", "services": [
        ("Eyebrows + Upper Lips", 45, 15, False, "Eyebrows and upper lips threading combo — ₹45."),
        ("Eyebrows + Upper Lips + Forehead", 60, 20, False, "Eyebrows, upper lips and forehead threading combo — ₹60."),
        ("Full Face Threading + Eyebrows", 150, 35, True, "Full face threading with eyebrows — ₹150."),
    ]},
    {"name": "Hand & Foot Care", "description": "Manicure and pedicure treatments for polished hands and feet.", "services": [
        ("Basic Manicure", 250, 40, False, "Basic manicure — ₹250."),
        ("Spa Manicure", 450, 60, True, "Spa manicure — ₹450."),
        ("Basic Pedicure", 350, 50, False, "Basic pedicure — ₹350."),
        ("Spa Pedicure", 550, 70, True, "Spa pedicure — ₹550."),
        ("Manicure + Pedicure Combo", 650, 90, True, "Manicure and pedicure combo — ₹650."),
    ]},
    {"name": "Other Services", "description": "Useful finishing, wash and draping services.", "services": [
        ("Head Massage with Oil", 200, 30, False, "Head massage with oil — ₹200."),
        ("Hair Wash", 150, 20, False, "Hair wash — ₹150."),
        ("Blow Dry", 250, 30, False, "Blow dry — ₹250."),
        ("Saree Draping", 150, 20, False, "Saree draping — ₹150."),
        ("Dupatta Setting", 100, 15, False, "Dupatta setting — ₹100."),
    ]},
    
]


class Command(BaseCommand):
    help = "Seeds the database with initial service categories, services, and site settings."

    def handle(self, *args, **options):
        # --- Site settings ---
        site = SiteSettings.load()
        logo_path = os.path.join(dj_settings.BASE_DIR, "static", "images", "logo.jpeg")
        if not site.logo and os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                site.logo.save("logo.jpeg", File(f), save=False)
        site.save()
        self.stdout.write(self.style.SUCCESS("Site settings ready."))

        # --- Categories & services ---
        for order, cat_data in enumerate(CATEGORY_DATA):
            category, _ = ServiceCategory.objects.update_or_create(
                name=cat_data["name"],
                defaults={"description": cat_data["description"], "order": order, "is_active": True},
            )
            for s_order, (name, price, duration, featured, desc) in enumerate(cat_data["services"]):
                Service.objects.update_or_create(
                    name=name,
                    defaults={
                        "category": category,
                        "price": price,
                        "duration_minutes": duration,
                        "is_featured": featured,
                        "short_description": desc[:120],
                        "description": desc,
                        "order": s_order,
                        "is_active": True,
                    },
                )

        # Hide the broad placeholder groups used by older versions of this seed
        # command. Their real services are now organised in the detailed groups
        # above; custom categories created in the admin are left untouched.
        retired_names = ["Hair Styling & Treatments", "Skin & Body Care", "Nail Art & Care"]
        retired_categories = ServiceCategory.objects.filter(name__in=retired_names)
        Service.objects.filter(category__in=retired_categories).update(is_active=False)
        retired_categories.update(is_active=False)
        self.stdout.write(self.style.SUCCESS(
            f"Seeded {ServiceCategory.objects.count()} categories and {Service.objects.count()} services."
        ))
        self.stdout.write(self.style.WARNING(
            "Next: log into /admin/ to add gallery photos, team members, testimonials and adjust prices."
        ))