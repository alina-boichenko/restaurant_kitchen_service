from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from kitchen.models import Cook, Dish


class CookCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "years_of_experience",

        )


class ModifiedImageField(forms.ImageField):
    image_validator = FileExtensionValidator(
        allowed_extensions=["jpg"],
        message="File extension not allowed. Allowed extensions include  .jpg"
    )
    default_validators = ["image_validator"]


class DishForm(forms.ModelForm):
    dish_image = ModifiedImageField()
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Dish
        fields = "__all__"

    def clean_price(self):
        price = self.cleaned_data["price"]

        if price < 0:
            raise ValidationError("Price must be greater than 0.")

        return price
