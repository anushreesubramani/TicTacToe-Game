#TicTacToe - 2 Player game

## Set-Up Instructions:
1.  Update the value of application in app.yaml to the app ID you have registered
 in the App Engine admin console and would like to use to host your instance of this sample.
2.  Run the app with the devserver using dev_appserver.py DIR, and ensure it's
 running by visiting the API Explorer - by default localhost:8080/_ah/api/explorer.
3.  (Optional) Generate your client library(ies) with the endpoints tool.
 Deploy your application.


##Game Description:

TicTacToe is an API engine based on python and Google App Engine.
It is a two player game. Each game begins with a 9X9 grid(play board) in which 2 players take turns to fill out X and O. The first player to get 3 X's or 3 O's in a straight line(horizontally,vertically or diagonally) wins the game.
The player inputs are sent to the `make_move` endpoint which will reply
with all the moves made on the board, whose turn it is next, whether the game is over and if yes then the winner of the Game.
 Each game can be retrieved or played by using the path parameter
`urlsafe_game_key`.

##Files Included:
 - api.py: Contains endpoints and game playing logic.
 - app.yaml: App configuration.
 - cron.yaml: Cronjob configuration.
 - main.py: Handler for taskqueue handler.
 - models.py: Entity and message definitions including helper methods.
 - utils.py: Helper function for retrieving ndb.Models by urlsafe Key string.

##Endpoints Included:
 - **create_user**
    - Path: 'user'
    - Method: POST
    - Parameters: user_name, email (optional)
    - Returns: Message confirming creation of the User.
    - Description: Creates a new User. user_name provided must be unique. Will
    raise a ConflictException if a User with that user_name already exists.

 - **new_game**
    - Path: 'game'
    - Method: POST
    - Parameters: player_x, player_o
    - Returns: GameForm with initial game state.
    - Description: Creates a new Game. player_x, player_o provided must correspond to usernames of an existing user - will raise a NotFoundException if not.

 - **get_game**
    - Path: 'game/{urlsafe_game_key}'
    - Method: GET
    - Parameters: urlsafe_game_key
    - Returns: GameForm with current game state.
    - Description: Returns the current state of a game.

 - **make_move**
    - Path: 'game/{urlsafe_game_key}'
    - Method: PUT
    - Parameters: urlsafe_game_key
    - Returns: GameForm with new game state.
    - Description: Accepts a 'move' which should range from integer value 1 to 9 depending on where the player wishes to place his move in the 3X3 grid. The 9 boxes in the 3X3 grid board are ordered from left to right, top to bottom in an ascending order. The 'player' refers to the user_name of the player making the move. By default, the game asks the player_x to make the first move. When the game comes to end, the winner is declared.
    Multiple validations are done in this api to ensure that the correct players are playing the game, no player plays out of turn, the players are registered users, the game has not been cancelled, the game isnt already over, the inputs for move are valid and not repetitive etc.
    Corresponding to these validations, appropriate messages are displayed in the response.

 - **get_user_games**
    - Path: 'game'
    - Method: GET
    - Parameters: username
    - Returns: GameForms with the list of all games that are active and the given user is a part of.
    - Description: Returns all games that are active and the given user is a part of. Will raise a NotFoundException if there are currently no active games for the given user. Will raise a NotFoundException if the User does not exist.

- **get_user_completed_games**
    - Path: 'get_user_completed_games'
    - Method: GET
    - Parameters: user_name
    - Returns: GameForms with the list of all games that have been completed and the given user was a part of.
    - Description: Returns all games that are completed and the given user was a part of. Will raise a NotFoundException if there are currently no completed games for the given user.
    Will raise a NotFoundException if the User does not exist.

 - **get_user_win_percent**
    - Path: 'get_user_win_percent'
    - Method: GET
    - Parameters: user_name
    - Returns: String containing the win percent.
    - Description: Returns the win percentage recorded by the provided player.
    Will raise a NotFoundException if the User does not exist.

 - **get_user_ranking**
    - Path: 'get_user_ranking'
    - Method: GET
    - Parameters: None
    - Returns: Leaderboard with user_name and corresponding win percentage
    - Description: Returns the username and win percent of all the users in descending order kinda like a leaderboard.

 - **game_history**
    - Path: 'games/game_history'
    - Method: GET
    - Parameters: urlsafe_game_key
    - Returns: History of moves made by each player and its result
    - Description: Returns output in the format: [(Player:X, Move: 1, Result: Move made)]
      In this way, the entire move history of the game is provided move by move.

 - **cancel_game**
    - Path: 'games/cancel'
    - Method: PUT
    - Parameters: urlsafe_game_key
    - Returns: Status whether the game was cancelled successfully
    - Description: This endpoint allows users to cancel a game in progress using the urlsafe_game_key.

##Models Included:
 - **User**
    - Stores unique user_name and (optional) email address.

 - **Game**
    - Stores unique game states. Associated with User model via KeyProperty.


##Forms Included:
 - **GameForm**
    - Representation of a Game's state (urlsafe_key, board,
    game_over flag, message, winner, player_x, player_o, next_turn).
 - **GameForms**
    - Multiple GameForm container.
 - **NewGameForm**
    - Used to create a new game (player_x, player_o)
 - **GameHistoryForm**
    - Representation of game history(game_history)
 - **MakeMoveForm**
    - Inbound make move form (move, player_name).
 - **UserForm**
    - UserForm for sending user ranking information (name, win_percent).
 - **UserForms**
    - Multiple UserForm container.
 - **StringMessage**
    - General purpose String container.
