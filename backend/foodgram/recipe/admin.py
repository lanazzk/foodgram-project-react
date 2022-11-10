from django.contrib import admin
from django.contrib.auth.models import Group
from recipe.models import (Favorite, Follow, Ingredient, IngredientInRecipe,
                           Recipe, Shopping_list, Tag)
from rest_framework.authtoken.models import TokenProxy


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )
    search_fields = ('name',)
    list_filter = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'name'
    )
    list_filter = ('author', 'name', 'tags')

    def is_favorited(self, obj):
        return obj.favorites.count()


admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientInRecipe)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite)
admin.site.register(Shopping_list)
admin.site.register(Follow)
admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
