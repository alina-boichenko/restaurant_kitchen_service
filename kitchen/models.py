from django.contrib.auth.models import AbstractUser
from django.db import models

from kitchen_service import settings


class Cook(AbstractUser):
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["username"]


class DishType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    dish_image = models.ImageField(
        null=True,
        blank=True,
        upload_to="images/",
        default="images/no_images_available.jpg"
    )
    dish_type = models.ForeignKey(
        DishType, on_delete=models.CASCADE, related_name="dishes"
    )
    cooks = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="dishes", blank=True
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "dishes"
