from rest_framework import serializers
from game.models import Game, Turn

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id',)

class TurnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turn
        fields = ('id', 'game', 'field_num')
