from rest_framework import serializers
from django.contrib.auth.models import User
from . import models
from django.db import transaction
from django.contrib.auth import hashers


class UserSerializer(serializers.ModelSerializer):
    balance = serializers.FloatField(source='profile.balance', default=0)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'balance')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        profile = validated_data.pop('profile')
        password = validated_data.pop('password')
        hashed_password = hashers.make_password(password)
        with transaction.atomic():
            user = User.objects.create(password=hashed_password, **validated_data)
            models.Profile.objects.create(user=user, **profile)
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email')
        instance.password = validated_data.get('password')
        instance.profile.balance = validated_data.get('balance')
        instance.save()
        return instance


class AnimalSerializer(serializers.ModelSerializer):
    kind = serializers.ChoiceField(choices=models.Animal.KINDS)
    class Meta:
        model = models.Animal
        fields = '__all__'


class BidSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Bid
        fields = '__all__'


class LotSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    bids = BidSerializer(many=True, required=False)

    class Meta:
        model = models.Lot
        fields = '__all__'

