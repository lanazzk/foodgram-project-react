from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (DownloadShoppingListApiView, FavoriteApiView,
                    FollowApiView, FollowListApiView, IngredientViewSet,
                    RecipeViewSet, ShoppingListApiView, TagViewSet)

app_name = 'api'

router_api = DefaultRouter()

router_api.register(r'recipes', RecipeViewSet, basename='recipes')
router_api.register(r'ingredients', IngredientViewSet, basename='ingredients')
router_api.register(r'tags', TagViewSet, basename='tags')


urlpatterns = [
    path('recipes/<int:recipe_id>/favorite/',
         FavoriteApiView.as_view(), name='favorite'),
    path('recipes/download_shopping_cart/',
         DownloadShoppingListApiView.as_view(),
         name='download_shopping_cart'),
    path('recipes/<int:recipe_id>/shopping_cart/',
         ShoppingListApiView.as_view()),
    path('users/<int:following_id>/subscribe/',
         FollowApiView.as_view()),
    path('users/subscriptions/',
         FollowListApiView.as_view(),
         name='subscriptions'),
    path('', include(router_api.urls)),
]
