from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.


class Game(models.Model):
    # Non-stored attribs
    field = [0 for i in range(9)]
    SYMS = (
        'X',
        'O'
    )

    # game end masks
    # TODO: more elegant
    WINNING = [
        [0, 1, 2],  # Across top
        [3, 4, 5],  # Across middle
        [6, 7, 8],  # Across bottom
        [0, 3, 6],  # Down left
        [1, 4, 7],  # Down middle
        [2, 5, 8],  # Down right
        [0, 4, 8],  # Diagonal ltr
        [2, 4, 6],  # Diagonal rtl
    ]

    @property
    def current_player(self, turn_num):
        "Returns player's id (player1/player2)"
        return self.SYMS[0] if turn_num % 2 else self.SYMS[1]

    def build_game(self):
        for i, turn in enumerate(self.turn_set.all()):
            self.field[turn.field_num - 1] = self.current_player(i)

    def is_over(self):
        for wins in self.WINNING:
            w = ''.join((self.field[pos] for pos in wins))
            for player in self.SYMS:
                if w == 3 * player:
                   return w
        # all moves done, no winner
        if len(self.field) == self.turn_set.count():
            return 'draw'
        return ''

    def correct_turn(self, field_num):
        try:
            return not self.field[field_num - 1]
        except IndexError:
            return False

# TODO: get player from API and check it before save
class Turn(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    field_num = models.IntegerField()

    def save(self, *args, **kwargs):
        self.game.build_game()
        finished = self.game.is_over()
        if self.game.correct_turn(self.field_num) or not finished:
            super(Turn, self).save(*args, **kwargs)
        else:
            raise ValidationError