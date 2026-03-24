from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class UserPaginationTests(TestCase):
    def setUp(self):
        self.admin_group, _ = Group.objects.get_or_create(name="Admin")
        self.participant_group, _ = Group.objects.get_or_create(name="Participant")
        self.admin = User.objects.create_user(username="admin", password="password123")
        self.admin.groups.add(self.admin_group)
        self.client.force_login(self.admin)

    def test_participant_list_is_paginated(self):
        for index in range(1, 11):
            user = User.objects.create_user(
                username=f"participant{index}",
                email=f"participant{index}@example.com",
                password="password123",
            )
            user.groups.add(self.participant_group)

        response = self.client.get(reverse("users:participants"), {"page": 2})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"].number, 2)
        self.assertEqual(len(response.context["participants"]), 1)
