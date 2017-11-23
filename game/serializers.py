from rest_framework import serializers
from game.models import Game, Turn


def add_winner(game, response):
    winner = game.get_winner()
    if winner:
        response['winner'] = winner


class GameSerializer(serializers.ModelSerializer):
    # DRF 3 not supports multiple SerializerMethodField()
    misc_data = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ('id', 'misc_data')

    def get_misc_data(self, obj):
        obj.build_game()

        response = {}
        response['field'] = obj.get_field()
        response['turns'] = [turn.field_num for turn in obj.turn_set.all()]

        add_winner(obj, response)

        return response


class TurnSerializer(serializers.ModelSerializer):
    client_data = serializers.SerializerMethodField()

    class Meta:
        model = Turn
        fields = ('id', 'game', 'field_num', 'client_data')

    def get_client_data(self, obj):
        obj.game.build_game()
        response = {}
        turn_num = obj.game.turn_set.count() - 1
        current_player = obj.game.current_player(turn_num)
        response['now_playing'] = current_player

        add_winner(obj.game, response)
        return response
