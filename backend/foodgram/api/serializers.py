import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from recipe.models import (Favorite, Follow, Ingredient, IngredientInRecipe,
                           Recipe, ShoppingList, Tag)
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.serializers import CurrentUserSerializer

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source='ingredient.id',
                                            read_only=True)
    name = serializers.StringRelatedField(source='ingredient.name',
                                          read_only=True)
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit', read_only=True)

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeGetSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientInRecipeSerializer(read_only=True, many=True)
    author = CurrentUserSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return (Favorite.objects.filter(user=user,
                                        recipe=obj).exists())

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return (ShoppingList.objects.filter(user=user,
                                            recipe=obj).exists())


class IngredientInRecipePostSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class RecipePostSerializer(serializers.ModelSerializer):
    ingredients = IngredientInRecipePostSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    image = Base64ImageField(required=False, allow_null=True)
    name = serializers.CharField(max_length=200)
    cooking_time = serializers.IntegerField(min_value=1)

    class Meta:
        model = Recipe
        fields = ('tags', 'ingredients', 'name', 'image',
                  'text', 'cooking_time')

    def add_ingredients(self, recipe, ingredients):
        for ingredient in ingredients:
            created, _ = IngredientInRecipe.objects.get_or_create(
                ingredient=get_object_or_404(
                    Ingredient,
                    id=ingredient['id'].pk),
                amount=ingredient['amount'])
            recipe.ingredients.add(created)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.add_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        instance.ingredients.clear()
        instance.tags.clear()
        instance.image = validated_data.get('image', instance.image)
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            self.add_ingredients(instance, ingredients)
        if 'tags' in validated_data:
            instance.tags.set(
                validated_data.pop('tags'))
        return super().update(
            instance, validated_data)

    def validate_ingredients(self, data):
        id_ingredients = []
        for ingredient in data:
            id_ingredients.append(ingredient['id'])
        if len(id_ingredients) > len(set(id_ingredients)):
            raise serializers.ValidationError(
                {'error': 'Ingredients should be unique'})
        return data

    def validate_tags(self, value):
        if len(value) < 1:
            raise serializers.ValidationError(
                {'error': 'At least one tag is required'})
        return value

    def validate_cooking_time(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                {'error': 'Cooking time should be more than 1'})
        return value

    def to_representation(self, instance):
        return RecipeGetSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }).data


class FavoriteShoppingGetSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('user', 'recipe')
        model = Favorite
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='Recipe already added to favorites'
            )
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        return FavoriteShoppingGetSerializer(
            instance.recipe,
            context={'request': request}
        ).data


class ShoppingListSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('user', 'recipe')
        model = ShoppingList
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingList.objects.all(),
                fields=('user', 'recipe'),
                message='Recipe already added to shopping list'
            )
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        return FavoriteShoppingGetSerializer(
            instance.recipe,
            context={'request': request}
        ).data


class FollowGetSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        model = User

    def get_is_subscribed(self, obj):
        return (Follow.objects.filter(
            user=self.context['request'].user,
            following=obj).exists()
        )

    def get_recipes(self, obj):
        recipes = obj.recipes.all()[:3]
        request = self.context.get('request')
        return FavoriteShoppingGetSerializer(
            recipes, many=True,
            context={'request': request}
        ).data

    def get_recipes_count(self, obj):
        return obj.recipes.all().count()


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]

    def validate(self, data):
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'You cannot suscribe to yourself')
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        return FollowGetSerializer(
            instance.following,
            context={'request': request}
        ).data
