from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from kitchen.models import DishType, Dish, Cook


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test123password",
        )

        self.client.force_login(self.admin_user)
        self.cook = get_user_model().objects.create_user(
            username="user_cook",
            password="pass123word",
            first_name="Test",
            last_name="Cook",
            years_of_experience=2
        )

        self.dish_type = DishType.objects.create(name="test")

        self.dish = Dish.objects.create(
            name="Test",
            ingredients="Test test test",
            description="How to cook?",
            price=150.00,
            dish_type=self.dish_type,
        )
        cook_test = Cook.objects.all()
        self.dish.cooks.set(cook_test)

    def test_cook_experience_listed(self):
        url = reverse("admin:kitchen_cook_changelist")
        result = self.client.get(url)

        self.assertContains(result, "Years of experience")

    def test_cook_detailed_experience_listed(self):
        url = reverse("admin:kitchen_cook_change", args=[self.cook.id])
        result = self.client.get(url)

        self.assertContains(result, "Years of experience")

    def test_add_new_cook(self):
        url = reverse("admin:kitchen_cook_add")
        result = self.client.get(url)

        self.assertContains(result, "First name:")
        self.assertContains(result, "Last name:")
        self.assertContains(result, "Years of experience")

    def test_dish_listed(self):
        url = reverse("admin:kitchen_dish_changelist")
        result = self.client.get(url)

        self.assertContains(result, self.dish.name)
        self.assertContains(result, self.dish.price)
        self.assertContains(result, self.dish.dish_type)
