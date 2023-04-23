from django.contrib.auth import get_user_model
from django.test import TestCase

from kitchen.models import DishType, Dish, Cook


class ModelsTests(TestCase):

    def setUp(self) -> None:

        self.cook = get_user_model().objects.create_user(
            username="cook",
            password="pass123word",
            first_name="Test",
            last_name="Cook",
            years_of_experience="2"
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

    def test_cook_str(self):
        self.assertEqual(
            str(self.cook), f"{self.cook.first_name} {self.cook.last_name}"
        )

    def test_dish_type_str(self):
        self.assertEqual(str(self.dish_type), self.dish_type.name)

    def test_dish_str(self):
        self.assertEqual(str(self.dish), self.dish.name)
