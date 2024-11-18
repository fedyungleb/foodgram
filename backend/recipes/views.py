from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response

from .filters import RecipeFilter
from .models import FavoriteRecipe, Ingredient, Recipe, ShoppingCart, Tag
from .permissions import AuthorOrReadOnly
from .serializers import (FavoritedSerializer, IngredientSerializer,
                          RecipeSerializer, ShoppingCartSerializer,
                          TagSerializer)
from .utils import get_shopping_list
from .external_api import ExternalGroceryService


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_class = RecipeFilter
    serializer_class = RecipeSerializer
    permission_classes = [AuthorOrReadOnly]

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticatedOrReadOnly],
        url_path='favorite'
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            favorite_recipe, created = FavoriteRecipe.objects.get_or_create(
                user=user, recipe=recipe
            )
            if created is True:
                serializer = FavoritedSerializer()
                return Response(
                    serializer.to_representation(instance=favorite_recipe),
                    status=status.HTTP_201_CREATED
                )
        if request.method == 'DELETE':
            FavoriteRecipe.objects.filter(
                user=user,
                recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticatedOrReadOnly]
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            recipe, created = ShoppingCart.objects.get_or_create(
                user=user, recipe=recipe
            )
            if created is True:
                serializer = ShoppingCartSerializer()
                return Response(
                    serializer.to_representation(instance=recipe),
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {'errors': 'Рецепт уже в корзине покупок'},
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            ShoppingCart.objects.filter(
                user=user, recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['GET'],
        url_path='download_shopping_cart',
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        try:
            return get_shopping_list(request)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['POST'],
        url_path='checkout',
        permission_classes=[IsAuthenticated]
    )
    def checkout(self, request):
        shopping_cart_items = ShoppingCart.objects.filter(user=request.user)
        if not shopping_cart_items.exists():
            return Response({"error": "Shopping cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        ingredients = {}
        for item in shopping_cart_items:
            recipe_ingredients = item.recipe.recipe_ingredients.all()
            for ingredient in recipe_ingredients:
                name = ingredient.ingredient.name
                unit = ingredient.ingredient.measurement_unit
                amount = ingredient.amount
                if name in ingredients:
                    ingredients[name]['quantity'] += amount
                else:
                    ingredients[name] = {
                        'name': name,
                        'quantity': amount,
                        'unit': unit,
                    }

        items = list(ingredients.values())

        grocery_service = ExternalGroceryService()
        response = grocery_service.create_shopping_list(items)

        if "error" in response:
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(response, status=status.HTTP_200_OK)


class IngredientsViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class TagsViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
