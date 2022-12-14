from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from recipe.models import Ingredient, Recipe, Tag

User = get_user_model()


class IngredientsSearchFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name', )


class RecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )
    is_favorited = filters.BooleanFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value in [True, '1']:
            return queryset.filter(favorites__user=user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value in [True, '1']:
            return queryset.filter(shopping_list__user=user)
        return queryset
