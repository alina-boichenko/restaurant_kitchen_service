from django.test import TestCase

from kitchen.forms import CookCreationForm, DishForm
from kitchen.models import DishType


class FormsTest(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "user_cook",
            "password1": "pass123word",
            "password2": "pass123word",
            "email": "user@cook.com",
            "first_name": "Test",
            "last_name": "Cook",
            "years_of_experience": 2
        }

    def test_cook_creation_form_with_fields_is_valid(self):
        form = CookCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_dish_price_is_not_negative(self):
        dish_type = DishType.objects.create(name="dish type1")
        dish_data = {
            "name": "test1",
            "ingredients": "test1",
            "description": "test1",
            "price": -300,
            "dish_type": dish_type
        }

        form = DishForm(data=dish_data)
        self.assertFalse(form.is_valid())
