from djoser.serializers import UserCreateSerializer
from rest_framework import serializers, validators

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from users.mixins import IsSubscribedMixin

from .models import CustomUser, Follow


class UserRegistrationSerializer(UserCreateSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password'
                  )
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomUserSerializer(serializers.ModelSerializer, IsSubscribedMixin):
    username = serializers.CharField(
        required=True,
        validators=[validators.UniqueValidator(
            queryset=CustomUser.objects.all()
        )]
    )

    class Meta:
        fields = [
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        ]
        model = CustomUser


class UserSubscribeSerializer(serializers.ModelSerializer, IsSubscribedMixin):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField('get_recipes_count')
    username = serializers.CharField(
        required=True,
        validators=[validators.UniqueValidator(
            queryset=CustomUser.objects.all()
        )]
    )

    class Meta:
        model = CustomUser
        fields = [
            'email', 'id', 'username', 'first_name', 'last_name',
            'recipes', 'recipes_count', 'is_subscribed'
        ]

    def validate(self, data):
        author = data['followed']
        user = data['follower']
        if user == author:
            raise serializers.ValidationError('You can`t follow for yourself!')
        if Follow.objects.filter(author=author, user=user).exists():
            raise serializers.ValidationError('You have already subscribed!')
        return data

    def create(self, validated_data):
        subscribe = Follow.objects.create(**validated_data)
        subscribe.save()
        return subscribe

    def get_recipes_count(self, data):
        return Recipe.objects.filter(author=data).count()

    def get_recipes(self, data):
        recipes_limit = self.context.get('request').GET.get('recipes_limit')
        recipes = (
            data.recipes.all()[:int(recipes_limit)]
            if recipes_limit else data.recipes
        )
        serializer = serializers.ListSerializer(child=RecipeSerializer())
        return serializer.to_representation(recipes)