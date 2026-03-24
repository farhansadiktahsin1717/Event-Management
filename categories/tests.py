from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from .models import Category


User = get_user_model()


class CategoryPaginationTests(TestCase):
    def setUp(self):
        organizer_group, _ = Group.objects.get_or_create(name="Organizer")
        self.organizer = User.objects.create_user(username="organizer", password="password123")
        self.organizer.groups.add(organizer_group)
        self.client.force_login(self.organizer)

    def test_category_list_is_paginated(self):
        for index in range(1, 10):
            Category.objects.create(
                name=f"Category {index}",
                description="Used to verify pagination across category listings.",
            )

        response = self.client.get(reverse("categories:list"), {"page": 2})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"].number, 2)
        self.assertEqual(len(response.context["categories"]), 1)
