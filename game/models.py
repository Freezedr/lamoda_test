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

    def get_field(self):
        return self.field

    def get_turns(self):
        return self.turn_set.all()

    def current_player(self, turn_num):
        """Returns player's id (player1/player2)"""
        return self.SYMS[0] if turn_num % 2 else self.SYMS[1]

    def build_game(self):
        self.field = [0 for i in range(9)]
        for i, turn in enumerate(self.turn_set.all()):
            self.field[turn.field_num - 1] = self.current_player(i - 1)

    def get_winner(self):
        for wins in self.WINNING:
            w = ''.join((str(self.field[pos]) for pos in wins))
            for player in self.SYMS:
                if w == 3 * player:
                    return player
        # all moves done, no winner
        if len(self.field) == self.turn_set.count():
            return 'draw'
        return ''

    def correct_turn(self, field_num):
        try:
            return not self.field[field_num - 1]
        except IndexError:
            return False


class Turn(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    field_num = models.IntegerField()

    def save(self, *args, **kwargs):
        self.game.build_game()
        winner = self.game.get_winner()
        if self.game.correct_turn(self.field_num) and not winner:
            super(Turn, self).save(*args, **kwargs)
        else:
            raise ValidationError('Incorrect turn')
