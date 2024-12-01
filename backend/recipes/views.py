from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
)
from rest_framework.response import Response

from foodgram import settings
from .filters import RecipeFilter
from .models import FavoriteRecipe, Ingredient, Recipe, ShoppingCart, Tag
from .permissions import AuthorOrReadOnly
from .serializers import (FavoritedSerializer, IngredientSerializer,
                          RecipeSerializer, ShoppingCartSerializer,
                          TagSerializer)
from .utils import get_shopping_list
from .external_api import ExternalGroceryService
import openai
from rest_framework.decorators import api_view



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

    @action(
        detail=False,  # Collection-level action
        methods=['POST'],
        permission_classes=[AllowAny],
        url_path='ai-suggestion'
    )
    def ai_suggest_recipe(self, request):
        import logging
        logger = logging.getLogger(__name__)

        try:
            logger.info(f"Headers: {request.headers}")
            logger.info(f"Body: {request.body}")
            logger.info(f"Parsed Data: {request.data}")

            # Step 1: Extract ingredients
            ingredients = request.data.get('ingredients', '')
            if not ingredients:
                logger.error("Ingredients missing in request")
                return Response({"error": "Ingredients list is required"}, status=400)

            # Step 2: Create prompt
            try:
                prompt = settings.AI_SUGGESTION_PROMPT_TEMPLATE.format(ingredients=ingredients)
            except Exception as e:
                logger.exception("Error formatting the prompt")
                return Response({"error": "Error formatting the AI prompt"}, status=500)

            # Step 3: Call OpenAI API
            try:
                openai.api_key = settings.OPENAI_API_KEY
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=200,
                )
                logger.info(f"OpenAI Response: {response}")
            except Exception as e:
                logger.exception("Error calling OpenAI API")
                return Response({"error": "Error interacting with OpenAI API"}, status=500)

            # Step 4: Parse OpenAI response
            try:
                suggestion = response["choices"][0]["message"]["content"]
                logger.info(f"Suggestion: {suggestion}")
                return Response({"success": True, "suggestion": suggestion})
            except KeyError as e:
                logger.exception("Error parsing OpenAI response")
                return Response({"error": "Unexpected response format from OpenAI"}, status=500)

        except Exception as e:
            logger.exception("Unhandled exception in AI suggestion view")
            return Response({"error": str(e)}, status=500)


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
