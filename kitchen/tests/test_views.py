import tempfile

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import DishType, Dish, Cook


class PublicTestsView(TestCase):
    def setUp(self) -> None:
        self.cook = get_user_model().objects.create_user(
            username="test_cook"
        )
        self.cook1 = get_user_model().objects.create_user(
            username="test_user"
        )

        self.dish_type = DishType.objects.create(name="test")
        self.dish_type1 = DishType.objects.create(name="new dish type")

        self.dish = Dish.objects.create(
            name="test",
            ingredients="test ingredients",
            description="test description",
            price=100.00,
            dish_type=self.dish_type,
            dish_image=tempfile.NamedTemporaryFile(suffix=".jpg").name
        )

    def test_search_dish_type_by_name(self):
        url = reverse("kitchen:dish-type-list")
        result = self.client.get(url + "?name=new")

        dish_types = DishType.objects.filter(name__icontains="new")

        self.assertTemplateUsed(result, "kitchen/dish_type_list.html")
        self.assertEqual(
            list(result.context["dish_type_list"]),
            list(dish_types)
        )

    def test_search_dish_by_name(self):
        url = reverse("kitchen:dish-list")
        result = self.client.get(url + "?name=t")

        dish_types = Dish.objects.filter(name__icontains="t")

        self.assertTemplateUsed(result, "kitchen/dish_list.html")
        self.assertEqual(
            list(result.context["dish_list"]),
            list(dish_types)
        )

    def test_search_cook_by_username(self):
        url = reverse("kitchen:cook-list")
        result = self.client.get(url + "?username=us")

        dish_types = Cook.objects.filter(username__icontains="us")

        self.assertTemplateUsed(result, "kitchen/cook_list.html")
        self.assertEqual(
            list(result.context["cook_list"]),
            list(dish_types)
        )

    def test_login_required_dish_type_create_view(self):
        url = reverse("kitchen:dish-type-create")
        result = self.client.get(url)

        self.assertNotEqual(result.status_code, 200)
        self.assertRedirects(
            result,
            "/accounts/login/?next=/dish-types/create/"
        )

    def test_login_required_dish_create_view(self):
        url = reverse("kitchen:dish-create")
        result = self.client.get(url)

        self.assertNotEqual(result.status_code, 200)
        self.assertRedirects(result, "/accounts/login/?next=/dishes/create/")

    def test_login_required_dish_type_update_view(self):
        url = reverse("kitchen:dish-type-update", args=[self.dish_type.pk])
        result = self.client.get(url)

        self.assertNotEqual(result.status_code, 200)
        self.assertRedirects(
            result,
            f"/accounts/login/?next=/dish-types/{self.dish.pk}/update/"
        )

    def test_login_required_dish_update_view(self):
        url = reverse("kitchen:dish-update", args=[self.dish.pk])
        result = self.client.get(url)

        self.assertNotEqual(result.status_code, 200)
        self.assertRedirects(
            result,
            f"/accounts/login/?next=/dishes/{self.dish.pk}/update/"
        )

    def test_login_required_cook_update_view(self):
        url = reverse("kitchen:cook-update", args=[self.cook.pk])
        result = self.client.get(url)

        self.assertNotEqual(result.status_code, 200)
        self.assertRedirects(
            result,
            f"/accounts/login/?next=/cooks/{self.cook.pk}/update/"
        )

    def test_login_required_dish_type_delete_view(self):
        url = reverse("kitchen:dish-type-delete", args=[self.dish_type.pk])
        result = self.client.get(url)

        self.assertNotEqual(result.status_code, 200)
        self.assertRedirects(
            result,
            f"/accounts/login/?next=/dish-types/{self.dish.pk}/delete/"
        )

    def test_login_required_dish_delete_view(self):
        url = reverse("kitchen:dish-delete", args=[self.dish.pk])
        result = self.client.get(url)

        self.assertNotEqual(result.status_code, 200)
        self.assertRedirects(
            result,
            f"/accounts/login/?next=/dishes/{self.dish.pk}/delete/"
        )

    def test_login_required_cook_delete_view(self):
        url = reverse("kitchen:cook-delete", args=[self.cook.pk])
        result = self.client.get(url)

        self.assertNotEqual(result.status_code, 200)
        self.assertRedirects(
            result,
            f"/accounts/login/?next=/cooks/{self.cook.pk}/delete/"
        )


class PrivateTestsView(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user_test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_create_dish_type(self):
        form_data = {
            "name": "test1",
        }

        self.client.post(reverse("kitchen:dish-type-create"), data=form_data)
        new_dish_type = DishType.objects.get(name=form_data["name"])

        self.assertEqual(new_dish_type.name, form_data["name"])

    def test_create_cook(self):
        form_data = {
            "username": "new_user",
            "password1": "passnew123us",
            "password2": "passnew123us",
            "first_name": "New",
            "last_name": "User",
            "email": "email@user.com",
            "years_of_experience": 2
        }

        self.client.post(reverse("kitchen:cook-create"), data=form_data)
        new_cook = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_cook.username, form_data["username"])
        self.assertEqual(new_cook.first_name, form_data["first_name"])
        self.assertEqual(new_cook.last_name, form_data["last_name"])
        self.assertEqual(new_cook.email, form_data["email"])
        self.assertEqual(
            new_cook.years_of_experience,
            form_data["years_of_experience"]
        )

    def test_add_or_delete_dish(self):
        dish_type = DishType.objects.create(name="test2")
        self.dish = Dish.objects.create(
            name="test",
            ingredients="test ingredients",
            description="test description",
            price=100.00,
            dish_type=dish_type,
        )

        url = reverse("kitchen:add-dish", args=[self.dish.pk])

        result = self.client.get(url)
        self.assertIn(self.user, self.dish.cooks.all())
        self.assertEqual(result.status_code, 302)

        result = self.client.get(url)
        self.assertEqual(result.status_code, 302)
        self.assertNotIn(self.user, self.dish.cooks.all())
