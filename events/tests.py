from datetime import date, time, timedelta

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from categories.models import Category

from .models import Event


class EventExperienceTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Conference", description="Professional events")

    def create_event(self, index):
        return Event.objects.create(
            name=f"Event {index}",
            description="A polished event listing for pagination tests.",
            date=date.today() + timedelta(days=index),
            time=time(hour=9, minute=0),
            location=f"Venue {index}",
            category=self.category,
        )

    def test_homepage_event_list_is_paginated(self):
        for index in range(1, 8):
            self.create_event(index)

        response = self.client.get(reverse("events:list"), {"page": 2})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"].number, 2)
        self.assertEqual(len(response.context["events"]), 1)

    def test_contact_form_sends_email_and_redirects(self):
        response = self.client.post(
            reverse("events:list"),
            {
                "name": "Avery Recruiter",
                "email": "avery@example.com",
                "message": "I would like to see a demo of the platform.",
            },
        )

        self.assertRedirects(response, f"{reverse('events:list')}#contact", fetch_redirect_response=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Avery Recruiter", mail.outbox[0].subject)
        self.assertEqual(mail.outbox[0].reply_to, ["avery@example.com"])

    @override_settings(DEBUG=False)
    def test_custom_404_page_is_rendered(self):
        response = self.client.get("/missing-page/")

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "The page you were looking for is not here.", status_code=404)
