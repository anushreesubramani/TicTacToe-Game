"""models.py - This file contains the class definitions for the Datastore
entities used by the Game. Because these classes are also regular Python
classes they can include methods (such as 'to_form' and 'new_game')."""

import random
from datetime import date
from protorpc import messages
from google.appengine.ext import ndb


class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    #  Email is an optional field for User
    email = ndb.StringProperty()

    def __eq__(self, other) :
        return self.__dict__ == other.__dict__


class Game(ndb.Model):
    """Game object"""
    winner = ndb.IntegerProperty(required=True, default="")
    next_turn = ndb.IntegerProperty(required=True, default="")
    game_over = ndb.BooleanProperty(required=True, default=False)
    board = ndb.JsonProperty(required=True, default="['','','','','','','','','']")
    player_x = ndb.KeyProperty(required=True, kind='User')
    player_o = ndb.KeyProperty(required=True, kind='User')


    @classmethod
    def new_game(cls, player_x, player_o):
        """Creates and returns a new game"""
        game = Game(player_x=player_x,
                    player_o=player_o,
                    game_over=False)
        game.put()
        return game

    def to_form(self, message):
        """Returns a GameForm representation of the Game"""
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.player_x = self.player_x.get().name
        form.player_o = self.player_o.get().name
        form.game_over = self.game_over
        form.next_turn = self.next_turn
        form.board = self.board
        form.winner = self.winner
        form.message = message
        return form

#     def end_game(self, won=False):
#         """Ends the game - if won is True, the player won. - if won is False,
#         the player lost."""
#         self.game_over = True
#         self.put()
#         # Add the game to the score 'board'
#         score = Score(user=self.user, date=date.today(), won=won,
#                       guesses=self.attempts_allowed - self.attempts_remaining)
#         score.put()


# class Score(ndb.Model):
#     """Score object"""
#     user = ndb.KeyProperty(required=True, kind='User')
#     date = ndb.DateProperty(required=True)
#     won = ndb.BooleanProperty(required=True)
#     guesses = ndb.IntegerProperty(required=True)

#     def to_form(self):
#         return ScoreForm(user_name=self.user.get().name, won=self.won,
#                          date=str(self.date), guesses=self.guesses)


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    # urlsafe_key = messages.StringField(1, required=True)
    # attempts_remaining = messages.IntegerField(2, required=True)
    # game_over = messages.BooleanField(3, required=True)
    # message = messages.StringField(4, required=True)
    # user_name = messages.StringField(5, required=True)

    game_over = messages.BooleanField(1, required=True)
    winner = messages.StringField(2, required=True)
    board = messages.StringField(3, required=True)
    next_turn = messages.StringField(4, required=True)
    player_x = messages.StringField(5, required=True)
    player_o = messages.StringField(6, required=True)
    urlsafe_key = messages.StringField(7, required=True)


class NewGameForm(messages.Message):
    """Used to create a new game"""
    # user_name = messages.StringField(1, required=True)
    player_x = messages.StringField(1, required=True)
    player_o = messages.StringField(2, required=True)
    # attempts = messages.IntegerField(4, default=5)


# class MakeMoveForm(messages.Message):
#     """Used to make a move in an existing game"""
#     move = messages.IntegerField(1, required=True)
#     player_name = messages.StringField(2, required=True)
#     urlsafe_game_key = messages.StringField(3, required=True)
#     user_name = messages.StringField(4, required=True)



# class ScoreForm(messages.Message):
#     """ScoreForm for outbound Score information"""
#     user_name = messages.StringField(1, required=True)
#     date = messages.StringField(2, required=True)
#     won = messages.BooleanField(3, required=True)
#     guesses = messages.IntegerField(4, required=True)


# class ScoreForms(messages.Message):
#     """Return multiple ScoreForms"""
#     items = messages.MessageField(ScoreForm, 1, repeated=True)


# class StringMessage(messages.Message):
#     """StringMessage-- outbound (single) string message"""
#     message = messages.StringField(1, required=True)
