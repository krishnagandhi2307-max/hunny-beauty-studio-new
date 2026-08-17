# Hunny's Makeover Studio — Website

A full-featured, dynamic salon/makeup-studio website built with **Django** and **MySQL**.
Every piece of content — services, prices, gallery photos, team members, testimonials,
site text, contact info, social links — is managed from the **Django admin panel**, with
no code changes needed.

---

## ✨ Features

- **Fully dynamic content** via the Django admin: services & categories, pricing, gallery,
  team, testimonials, bookings, contact messages, and global site settings (hero text,
  about text, phone/email/address, socials, opening hours) — all editable without touching code.
- **Online booking system** — clients pick a service, date, time and location (studio/home);
  requests land in the admin with a status you can move through Pending → Confirmed → Completed.
- **Contact form** that stores messages in the database, visible in the admin.
- **Service catalog** with categories, filtering, search, and individual detail pages.
- **Portfolio gallery** with category filters, pagination, and a lightbox.
- **Testimonials** with star ratings and an admin approval workflow (only approved reviews show up).
- **Team / About page**.
- **Responsive, premium design** — nude / blush pink / white / rose-gold palette, Playfair
  Display + Jost typography, sticky nav, floating WhatsApp button, animated stats, etc.
- **MySQL** as the production database (via `mysqlclient`).
- Uses **WhiteNoise** to serve static files simply in production.

---

## 🗂 Project Structure

```
hunnys_studio/
├── hunnys_studio/        # Project settings, URLs
├── studio/                # Main app: models, views, admin, forms, urls
│   └── management/commands/seed_data.py   # Pre-loads categories/services from the brief
├── templates/             # All HTML templates (base.html + studio/*.html)
├── static/                # CSS, JS, logo image
├── media/                 # User-uploaded images (created at runtime)
├── requirements.txt
├── .env.example
└── manage.py
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- MySQL Server 8+ (running locally or remotely)
- (Recommended) a virtual environment

### 2. Install dependencies

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

> **Note on `mysqlclient`:** it needs MySQL's development headers to build.
> - Ubuntu/Debian: `sudo apt install default-libmysqlclient-dev pkg-config`
> - macOS: `brew install mysql-client pkg-config`
> - Windows: use the prebuilt wheel (`pip install mysqlclient` normally works with a recent pip).

### 3. Create the MySQL database

```sql
CREATE DATABASE hunnys_studio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'hunny_user'@'localhost' IDENTIFIED BY 'a_strong_password';
GRANT ALL PRIVILEGES ON hunnys_studio_db.* TO 'hunny_user'@'localhost';
FLUSH PRIVILEGES;
```

### 4. Configure environment variables

```bash
cp .env.example .env
```
Edit `.env` and set `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` to match
what you created above, and set a real `DJANGO_SECRET_KEY`.

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create an admin (superuser) account

```bash
python manage.py createsuperuser
```

### 7. Load starter content (optional but recommended)

This pre-fills the exact service list from the brief (Bridal Makeup, HD Makeup,
Hair Botox, Keratin Treatment, Nail Art, etc.) with categories and starter prices/durations,
plus the studio logo as the site logo — so the site looks complete on first run. You can
edit every price, description, and image afterwards from the admin.

```bash
python manage.py seed_data
```

### 8. Run the development server

```bash
python manage.py runserver
```

Visit:
- **Website:** http://127.0.0.1:8000/
- **Admin panel:** http://127.0.0.1:8000/admin/

---

## 🛠 Managing Content (for the studio owner)

Everything below is done from **`/admin/`** after logging in:

| What you want to change                          | Where in admin                     |
|---------------------------------------------------|-------------------------------------|
| Add/edit/remove a service or its price            | Studio Content → Services           |
| Add/edit a service category                        | Studio Content → Service Categories |
| Add gallery photos                                 | Studio Content → Gallery Images     |
| Add team members                                   | Studio Content → Team Members       |
| Approve a client review so it appears on the site  | Studio Content → Testimonials       |
| View/manage booking requests                        | Studio Content → Bookings           |
| View contact form messages                          | Studio Content → Contact Messages   |
| Change hero text, about text, phone, address, socials, logo | Studio Content → Site Settings (single record) |

The **WhatsApp number**, **phone**, **address**, **opening hours** and **all hero/about text**
are all controlled from **Site Settings** — update them once and they appear everywhere
(header, footer, floating WhatsApp button, contact page).

---

## 📦 Deploying to Production

1. Set `DJANGO_DEBUG=False` and set `DJANGO_ALLOWED_HOSTS` to your real domain(s).
2. Set a strong, unique `DJANGO_SECRET_KEY`.
3. Point `DB_HOST` etc. to your production MySQL instance.
4. Collect static files:
   ```bash
   python manage.py collectstatic
   ```
5. Run behind Gunicorn + Nginx (or your host of choice), e.g.:
   ```bash
   gunicorn hunnys_studio.wsgi:application --bind 0.0.0.0:8000
   ```
6. Configure your real SMTP credentials in `.env` if you want booking/contact
   email notifications instead of just database records + admin visibility.
7. Serve `MEDIA_ROOT` (uploaded images) via Nginx or a cloud storage backend
   (e.g. S3 via `django-storages`) for a scalable production setup.

---

## 🎨 Design Notes

- **Palette:** nude (#f4ece3), blush pink (#f2d7d6), white (#fffdfb), rose gold (#b7727c → #9c5964 gradient), gold accent (#c9a66b).
- **Typography:** Playfair Display (headings), Jost (body), Petit Formal Script (accents/eyebrows) — all from Google Fonts.
- **Signature motif:** the studio's own "H" monogram as a soft background watermark in the hero, echoing the logo.
- Fully responsive down to mobile, with a slide-in nav, reduced-motion support, and accessible focus states on form fields.

---

## 🔮 Ideas for Future Enhancements

- SMS/WhatsApp API integration to auto-notify clients when a booking is confirmed.
- Online payment for booking deposits (Razorpay/Stripe).
- Client login area to view past appointments.
- Loyalty/referral program tracking.
- Blog/beauty-tips section for SEO.

Feel free to ask for any of these to be added!
