from rest_framework import serializers
from .models import Role, GameParameters, Player


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class GameParametersSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameParameters
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'
