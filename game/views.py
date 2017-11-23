from game.models import Game, Turn
from rest_framework import viewsets
from game.serializers import GameSerializer, TurnSerializer
# Create your views here.


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class TurnViewSet(viewsets.ModelViewSet):
    queryset = Turn.objects.all()
    serializer_class = TurnSerializer
