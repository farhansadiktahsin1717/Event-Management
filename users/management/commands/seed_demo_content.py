from datetime import date, time, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from django.db import connection
from django.db import transaction
from django.utils.text import slugify

from categories.models import Category
from events.models import Event


User = get_user_model()


DEMO_CATEGORIES = [
    {
        "name": "Technology",
        "description": "Hackathons, startup showcases, product launches, and digital innovation events.",
    },
    {
        "name": "Business",
        "description": "Founder meetups, leadership summits, networking sessions, and pitch nights.",
    },
    {
        "name": "Culture",
        "description": "Art showcases, music gatherings, creative festivals, and storytelling experiences.",
    },
    {
        "name": "Wellness",
        "description": "Mindfulness sessions, wellness workshops, fitness events, and healthy community programs.",
    },
]

DEMO_GROUPS = [
    "Admin",
    "Organizer",
    "Participant",
    "Volunteer Crew",
    "Guest Speakers",
    "Community Partners",
]

DEMO_USERS = [
    {
        "username": "admin_demo",
        "email": "admin@eventmanagement.local",
        "first_name": "Nadia",
        "last_name": "Rahman",
        "phone_number": "+880 1711 100001",
        "password": "DemoPass123!",
        "group": "Admin",
    },
    {
        "username": "lina_organizer",
        "email": "lina@eventmanagement.local",
        "first_name": "Lina",
        "last_name": "Ahmed",
        "phone_number": "+880 1711 100002",
        "password": "DemoPass123!",
        "group": "Organizer",
    },
    {
        "username": "samir_organizer",
        "email": "samir@eventmanagement.local",
        "first_name": "Samir",
        "last_name": "Chowdhury",
        "phone_number": "+880 1711 100003",
        "password": "DemoPass123!",
        "group": "Organizer",
    },
    {
        "username": "maya_participant",
        "email": "maya@eventmanagement.local",
        "first_name": "Maya",
        "last_name": "Sultana",
        "phone_number": "+880 1711 100101",
        "password": "DemoPass123!",
        "group": "Participant",
    },
    {
        "username": "arif_participant",
        "email": "arif@eventmanagement.local",
        "first_name": "Arif",
        "last_name": "Hasan",
        "phone_number": "+880 1711 100102",
        "password": "DemoPass123!",
        "group": "Participant",
    },
    {
        "username": "sara_participant",
        "email": "sara@eventmanagement.local",
        "first_name": "Sara",
        "last_name": "Kabir",
        "phone_number": "+880 1711 100103",
        "password": "DemoPass123!",
        "group": "Participant",
    },
    {
        "username": "tanvir_participant",
        "email": "tanvir@eventmanagement.local",
        "first_name": "Tanvir",
        "last_name": "Islam",
        "phone_number": "+880 1711 100104",
        "password": "DemoPass123!",
        "group": "Participant",
    },
    {
        "username": "nabila_participant",
        "email": "nabila@eventmanagement.local",
        "first_name": "Nabila",
        "last_name": "Noor",
        "phone_number": "+880 1711 100105",
        "password": "DemoPass123!",
        "group": "Participant",
    },
    {
        "username": "farhan_participant",
        "email": "farhan@eventmanagement.local",
        "first_name": "Farhan",
        "last_name": "Mahmud",
        "phone_number": "+880 1711 100106",
        "password": "DemoPass123!",
        "group": "Participant",
    },
]

DEMO_EVENTS = [
    {
        "name": "FutureStack Tech Summit 2026",
        "description": "A modern one-day conference featuring AI product demos, founder talks, and practical workshops for builders.",
        "date_offset": 10,
        "time": time(10, 0),
        "location": "International Convention City, Dhaka",
        "category": "Technology",
        "participants": ["maya_participant", "arif_participant", "sara_participant", "farhan_participant"],
        "palette": ("#082F49", "#0F766E", "#67E8F9"),
        "eyebrow": "Innovation Summit",
    },
    {
        "name": "LaunchPad Founder Mixer",
        "description": "An evening networking session for entrepreneurs, investors, and startup operators with structured introductions.",
        "date_offset": 18,
        "time": time(18, 30),
        "location": "Gulshan LinkSpace, Dhaka",
        "category": "Business",
        "participants": ["maya_participant", "tanvir_participant", "nabila_participant"],
        "palette": ("#172554", "#1D4ED8", "#93C5FD"),
        "eyebrow": "Business Networking",
    },
    {
        "name": "City Canvas Art Night",
        "description": "A curated cultural evening with live illustration, installation art, photography walls, and creator conversations.",
        "date_offset": 26,
        "time": time(17, 0),
        "location": "Shilpakala Academy Plaza",
        "category": "Culture",
        "participants": ["arif_participant", "sara_participant", "nabila_participant", "farhan_participant"],
        "palette": ("#4C1D95", "#7C3AED", "#F0ABFC"),
        "eyebrow": "Creative Showcase",
    },
    {
        "name": "Reset Wellness Retreat",
        "description": "A calm half-day program with yoga, breathwork, healthy food stations, and guided reflection sessions.",
        "date_offset": 33,
        "time": time(8, 30),
        "location": "Hatirjheel Lakeside Pavilion",
        "category": "Wellness",
        "participants": ["maya_participant", "tanvir_participant", "nabila_participant", "farhan_participant"],
        "palette": ("#064E3B", "#059669", "#A7F3D0"),
        "eyebrow": "Wellness Experience",
    },
    {
        "name": "Product Demo Day Live",
        "description": "A recruiter-friendly showcase of product thinking, prototypes, demos, and audience feedback from emerging teams.",
        "date_offset": 42,
        "time": time(14, 0),
        "location": "Banani Innovation Hub",
        "category": "Technology",
        "participants": ["maya_participant", "arif_participant", "tanvir_participant", "sara_participant"],
        "palette": ("#111827", "#0EA5E9", "#F59E0B"),
        "eyebrow": "Product Showcase",
    },
    {
        "name": "Community Impact Forum",
        "description": "Panels and workshops on volunteer coordination, community partnerships, and designing events with local impact.",
        "date_offset": 55,
        "time": time(11, 0),
        "location": "BRAC Centre Inn",
        "category": "Business",
        "participants": ["arif_participant", "tanvir_participant", "nabila_participant"],
        "palette": ("#1F2937", "#F97316", "#FED7AA"),
        "eyebrow": "Community Forum",
    },
]


def event_svg(title, eyebrow, location, primary, secondary, accent):
    safe_title = title.replace("&", "&amp;")
    safe_eyebrow = eyebrow.replace("&", "&amp;")
    safe_location = location.replace("&", "&amp;")
    return f"""<svg width="1600" height="900" viewBox="0 0 1600 900" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="110" y1="80" x2="1460" y2="820" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{primary}"/>
      <stop offset="0.6" stop-color="{secondary}"/>
      <stop offset="1" stop-color="{accent}"/>
    </linearGradient>
  </defs>
  <rect width="1600" height="900" rx="42" fill="url(#bg)"/>
  <circle cx="1330" cy="180" r="190" fill="white" fill-opacity="0.09"/>
  <circle cx="1380" cy="700" r="250" fill="white" fill-opacity="0.08"/>
  <circle cx="260" cy="760" r="200" fill="white" fill-opacity="0.07"/>
  <rect x="96" y="96" width="1408" height="708" rx="34" fill="#FFFFFF" fill-opacity="0.08" stroke="white" stroke-opacity="0.14" stroke-width="2"/>
  <rect x="130" y="130" width="250" height="48" rx="24" fill="white" fill-opacity="0.16"/>
  <text x="165" y="162" fill="white" font-family="Arial, sans-serif" font-size="24" font-weight="700" letter-spacing="4">{safe_eyebrow.upper()}</text>
  <text x="132" y="320" fill="white" font-family="Arial, sans-serif" font-size="88" font-weight="700">{safe_title}</text>
  <text x="132" y="390" fill="white" fill-opacity="0.88" font-family="Arial, sans-serif" font-size="34" font-weight="500">Event Management Demo Collection</text>
  <text x="132" y="690" fill="white" fill-opacity="0.82" font-family="Arial, sans-serif" font-size="34" font-weight="600">{safe_location}</text>
  <path d="M132 730H540" stroke="white" stroke-opacity="0.55" stroke-width="8" stroke-linecap="round"/>
  <rect x="1124" y="584" width="246" height="146" rx="28" fill="white" fill-opacity="0.13"/>
  <circle cx="1198" cy="658" r="34" fill="white"/>
  <path d="M1198 641C1188.61 641 1181 648.611 1181 658C1181 673.084 1198 691 1198 691C1198 691 1215 673.084 1215 658C1215 648.611 1207.39 641 1198 641ZM1198 665.5C1193.86 665.5 1190.5 662.142 1190.5 658C1190.5 653.858 1193.86 650.5 1198 650.5C1202.14 650.5 1205.5 653.858 1205.5 658C1205.5 662.142 1202.14 665.5 1198 665.5Z" fill="{primary}"/>
  <text x="1260" y="648" fill="white" font-family="Arial, sans-serif" font-size="22" font-weight="700">Live Event</text>
  <text x="1260" y="680" fill="white" fill-opacity="0.8" font-family="Arial, sans-serif" font-size="18" font-weight="500">Demo poster image</text>
</svg>"""


def profile_svg(full_name, primary, accent):
    safe_name = full_name.replace("&", "&amp;")
    initials = "".join(part[0] for part in full_name.split()[:2]).upper()
    return f"""<svg width="600" height="600" viewBox="0 0 600 600" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="avatarBg" x1="40" y1="40" x2="560" y2="560" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{primary}"/>
      <stop offset="1" stop-color="{accent}"/>
    </linearGradient>
  </defs>
  <rect width="600" height="600" rx="120" fill="url(#avatarBg)"/>
  <circle cx="300" cy="228" r="94" fill="white" fill-opacity="0.22"/>
  <path d="M146 472C167.737 389.956 241.398 332 323 332C404.602 332 478.263 389.956 500 472V508H146V472Z" fill="white" fill-opacity="0.2"/>
  <text x="300" y="298" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="110" font-weight="700">{initials}</text>
  <text x="300" y="548" text-anchor="middle" fill="white" fill-opacity="0.88" font-family="Arial, sans-serif" font-size="34" font-weight="600">{safe_name}</text>
</svg>"""


class Command(BaseCommand):
    help = "Create polished demo categories, groups, users, events, and local SVG media assets."

    def handle(self, *args, **options):
        self.can_seed_rsvps = self.participant_table_targets_custom_user()
        with transaction.atomic():
            groups = self.create_groups()
            categories = self.create_categories()
            users = self.create_users(groups)
            events = self.create_events(categories, users)

        self.stdout.write(self.style.SUCCESS("Demo content created successfully."))
        self.stdout.write(
            f"Groups: {len(groups)}, Categories: {len(categories)}, Users: {len(users)}, Events: {len(events)}"
        )
        self.stdout.write("Shared password for demo accounts: DemoPass123!")
        if not self.can_seed_rsvps:
            self.stdout.write(
                self.style.WARNING(
                    "RSVP participant links were skipped because the existing join table still targets auth_user instead of users_user."
                )
            )

    def create_groups(self):
        groups = {}
        for group_name in DEMO_GROUPS:
            group, _ = Group.objects.get_or_create(name=group_name)
            groups[group_name] = group
        return groups

    def create_categories(self):
        categories = {}
        for payload in DEMO_CATEGORIES:
            category, _ = Category.objects.update_or_create(
                name=payload["name"],
                defaults={"description": payload["description"]},
            )
            categories[payload["name"]] = category
        return categories

    def create_users(self, groups):
        users = {}
        avatar_palette = [
            ("#082F49", "#0891B2"),
            ("#0F766E", "#F97316"),
            ("#1E3A8A", "#0EA5E9"),
            ("#4C1D95", "#A855F7"),
            ("#064E3B", "#22C55E"),
            ("#7C2D12", "#FB923C"),
        ]

        for index, payload in enumerate(DEMO_USERS):
            user, created = User.objects.get_or_create(
                username=payload["username"],
                defaults={
                    "email": payload["email"],
                    "first_name": payload["first_name"],
                    "last_name": payload["last_name"],
                    "phone_number": payload["phone_number"],
                    "is_active": True,
                },
            )

            for field in ["email", "first_name", "last_name", "phone_number"]:
                setattr(user, field, payload[field])
            user.is_active = True
            user.set_password(payload["password"])

            full_name = f"{payload['first_name']} {payload['last_name']}"
            primary, accent = avatar_palette[index % len(avatar_palette)]
            avatar_path = f"profiles/demo-{slugify(payload['username'])}.svg"
            self.store_svg(avatar_path, profile_svg(full_name, primary, accent))
            user.profile_picture.name = avatar_path
            user.save()

            user.groups.clear()
            user.groups.add(groups[payload["group"]])
            users[payload["username"]] = user

        return users

    def create_events(self, categories, users):
        events = {}
        base_date = date.today()

        for payload in DEMO_EVENTS:
            event, _ = Event.objects.update_or_create(
                name=payload["name"],
                defaults={
                    "description": payload["description"],
                    "date": base_date + timedelta(days=payload["date_offset"]),
                    "time": payload["time"],
                    "location": payload["location"],
                    "category": categories[payload["category"]],
                },
            )

            primary, secondary, accent = payload["palette"]
            image_path = f"events/demo-{slugify(payload['name'])}.svg"
            self.store_svg(
                image_path,
                event_svg(
                    payload["name"],
                    payload["eyebrow"],
                    payload["location"],
                    primary,
                    secondary,
                    accent,
                ),
            )
            event.image.name = image_path
            event.save()

            if self.can_seed_rsvps:
                participant_users = [users[username] for username in payload["participants"]]
                event.participants.set(participant_users)
            events[payload["name"]] = event

        return events

    def store_svg(self, relative_path, svg_markup):
        if default_storage.exists(relative_path):
            default_storage.delete(relative_path)
        default_storage.save(relative_path, ContentFile(svg_markup.encode("utf-8")))

    def participant_table_targets_custom_user(self):
        if connection.vendor != "sqlite":
            return True

        with connection.cursor() as cursor:
            rows = cursor.execute(
                "PRAGMA foreign_key_list('events_event_participants')"
            ).fetchall()

        user_targets = [row[2] for row in rows if row[3] == "user_id"]
        return not user_targets or user_targets[0] == "users_user"
