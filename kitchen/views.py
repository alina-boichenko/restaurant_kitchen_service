from django.shortcuts import render
from django.views.generic import ListView, DetailView

from kitchen.models import Cook, Dish, DishType


def index(request):
    num_dish_types = DishType.objects.count()
    num_dishes = Dish.objects.count()
    num_cooks = Cook.objects.count()

    context = {
        "num_dish_types": num_dish_types,
        "num_dishes": num_dishes,
        "num_cooks": num_cooks
    }
    return render(request, "kitchen/index.html", context=context)


class DishTypeListView(ListView):
    model = DishType
    template_name = "kitchen/dish_type_list.html"
    context_object_name = "dish_type_list"
    ordering = ["name"]


class DishTypeDetailView(DetailView):
    model = DishType
    template_name = "kitchen/dish_type_detail.html"
    context_object_name = "dish_type"


class DishListView(ListView):
    model = Dish
    ordering = ["name"]
    paginate_by = 5


class DishDetailView(DetailView):
    model = Dish


class CookListView(ListView):
    model = Cook
    paginate_by = 6


class CookDetailView(DetailView):
    model = Cook
    queryset = Cook.objects.prefetch_related("dishes")
