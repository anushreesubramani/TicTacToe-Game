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
    # score = ndb.IntegerProperty(default=0)

    def __eq__(self, other) :
        return self.__dict__ == other.__dict__


class Game(ndb.Model):
    """Game object"""
    winner = ndb.StringProperty(required=True, default="")
    next_turn = ndb.StringProperty(required=True, default="")
    game_over = ndb.BooleanProperty(required=True, default=False)
    board = ndb.JsonProperty(required=True, default=['-','-','-','-','-','-','-','-','-'])
    player_x = ndb.KeyProperty(required=True, kind='User')
    player_o = ndb.KeyProperty(required=True, kind='User')
    number_of_moves = ndb.IntegerProperty(required=True, default=0)
    history = ndb.JsonProperty(required=True, default=[])
    is_cancelled = ndb.BooleanProperty(required=True, default=False)


    @classmethod
    def new_game(cls, player_x, player_o, next_turn):
        """Creates and returns a new game"""
        game = Game(player_x=player_x,
                    player_o=player_o,
                    next_turn=next_turn,
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
        form.board = ','.join(self.board)
        form.winner = self.winner
        form.message = message
        return form

    def end_game(self, winner_key, loser_key, won=False):
        """Ends the game - if won is True, the player won. - if won is False,
        the player lost."""
        self.game_over = True
        self.put()
        # Add the game to the score 'board'
        if won:
            score = Score(user=winner_key, date=date.today(), won=won,
                          number_of_moves=self.number_of_moves,
                          score=(6 - self.number_of_moves))
            # score_o = Score(user=loser_key, date=date.today(), won=False,
            #               number_of_moves=self.number_of_moves)
        # else:
        #     # This is in case of a tie. There is no winner.
        #     # Consider Both of them to lose.
        #     score_x = Score(user=winner_key, date=date.today(), won=False,
        #                   number_of_moves=self.number_of_moves)
        #     score_o = Score(user=loser_key, date=date.today(), won=False,
        #                   number_of_moves=self.number_of_moves)
        score.put()
        # score_o.put()


class Score(ndb.Model):
    """Score object"""
    user = ndb.KeyProperty(required=True, kind='User')
    # user = ndb.StringProperty(required=True)
    # game = ndb.KeyProperty(required=True, kind='Game')
    date = ndb.DateProperty(required=True)
    won = ndb.BooleanProperty(required=True)
    number_of_moves = ndb.IntegerProperty(required=True, default=0)
    score = ndb.IntegerProperty(required=True, default=0)

    def to_form(self):
        return ScoreForm(user_name=self.user.get().name, date=str(self.date),
                         won=self.won,
                         number_of_moves=self.number_of_moves,
                         score=self.score)


class GameForm(messages.Message):
    """GameForm for outbound game state information"""

    game_over = messages.BooleanField(1, required=True)
    winner = messages.StringField(2, required=True)
    board = messages.StringField(3, required=True)
    next_turn = messages.StringField(4, required=True)
    player_x = messages.StringField(5, required=True)
    player_o = messages.StringField(6, required=True)
    urlsafe_key = messages.StringField(7, required=True)
    message = messages.StringField(8, required=True)

class GameForms(messages.Message):
    """Return multiple GameForms"""
    items = messages.MessageField(GameForm, 1, repeated=True)

class GameHistoryForm(messages.Message):
    '''Used to send the Game History information'''
    game_history = messages.StringField(1, required=True)


class NewGameForm(messages.Message):
    """Used to create a new game"""
    player_x = messages.StringField(1, required=True)
    player_o = messages.StringField(2, required=True)


class MakeMoveForm(messages.Message):
    """Used to make a move in an existing game"""
    move = messages.IntegerField(1, required=True)
    player_name = messages.StringField(2, required=True)


class ScoreForm(messages.Message):
    """ScoreForm for outbound Score information"""
    user_name = messages.StringField(1, required=True)
    date = messages.StringField(2, required=True)
    won = messages.BooleanField(3, required=True)
    number_of_moves = messages.IntegerField(4, required=True)
    score = messages.IntegerField(5, required=True)


class ScoreForms(messages.Message):
    """Return multiple ScoreForms"""
    items = messages.MessageField(ScoreForm, 1, repeated=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)
