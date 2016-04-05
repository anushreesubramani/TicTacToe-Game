#!/usr/bin/env python

"""main.py - This file contains handlers that are called by taskqueue and/or
cronjobs."""
import logging

import webapp2
from google.appengine.api import mail, app_identity
from api import TicTacToeApi
from google.appengine.ext import ndb

from models import User, Game


class SendReminderEmail(webapp2.RequestHandler):
    def get(self):
        """Send a reminder email to each User with an email about games.
        Called every hour using a cron job"""
        app_id = app_identity.get_application_id()
        games = Game.query(ndb.AND(Game.game_over==False, Game.is_cancelled==False))
        for game in games:
            subject = 'This is a gentle reminder!'
            user1 = game.player_x.get()
            if user1.email != None:
                body = 'Hello {}, try out our exciting new TicTacToe Game!'.format(user1.name)
                # This will send test emails, the arguments to send_mail are:
                # from, to, subject, body
                mail.send_mail('noreply@{}.appspotmail.com'.format(app_id),
                               user1.email,
                               subject,
                               body)
            user2 = game.player_o.get()
            if user2.email != None:
                body = 'Hello {}, try out our exciting new TicTacToe Game!'.format(user2.name)
                mail.send_mail('noreply@{}.appspotmail.com'.format(app_id),
                               user2.email,
                               subject,
                               body)


class UpdateAverageMovesRemaining(webapp2.RequestHandler):
    def post(self):
        """Update game listing announcement in memcache."""
        TicTacToeApi._cache_average_moves()
        self.response.set_status(204)

app = webapp2.WSGIApplication([
    ('/crons/send_reminder', SendReminderEmail),
    ('/tasks/cache_average_moves', UpdateAverageMovesRemaining),
], debug=True)
