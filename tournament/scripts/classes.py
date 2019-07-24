import sys
from tournament.scripts.constants import NUMBER_OF_SETS


class Participant:

    id = None
    name = None
    email = None
    games = None
    number_of_games = None
    rivals = None
    win_sets = None
    win_balls = None

    def __init__(self, id):
        self.id = id
        self.name = str(id)
        self.games = []
        self.number_of_games = 0
        self.rivals = []
        self.win_sets = 0
        self.win_balls = 0

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return self.id != other.id

    def set_name(self, name):
        self.name = name

    def set_email(self, email):
        self.email = email.split("@")[0] + "@appliedtech.ru"

    def add_game(self, game):
        self.games.append(game)
        self.number_of_games += 1

        if isinstance(game.player1, Participant):
            if self == game.player1:
                self.rivals.append(game.player2)
            else:
                self.rivals.append(game.player1)
        else:
            if self == game.player1.participant1 or self == game.player1.participant2:
                self.rivals.append(game.player2.participant1)
                self.rivals.append(game.player2.participant2)
            else:
                self.rivals.append(game.player1.participant1)
                self.rivals.append(game.player1.participant2)

    def add_sets(self, n):
        self.win_sets += n

    def add_balls(self, n):
        self.win_balls += n

    def duplicate_rivals(self):
        duplicates = {}
        for rival in self.rivals:
            if self.rivals.count(rival) > 1:
                duplicates[str(rival)] = self.rivals.count(rival)
        return duplicates

    def duplicate_count(self, rival):
        return self.rivals.count(rival)

    def duplicates_count(self):
        duplicates = self.duplicate_rivals()
        return len(duplicates.keys())


class Couple:

    # Can be either rivals or partners
    participant1 = None
    participant2 = None

    def __init__(self, p1, p2):
        if p1.id < p2.id:
            self.participant1 = p1
            self.participant2 = p2
        elif p1.id > p2.id:
            self.participant1 = p2
            self.participant2 = p1
        else:
            sys.exit("Error: couple consists of the same participant: " + str(p1))

    def __str__(self):
        return str(self.participant1) + ", " + str(self.participant2)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.participant1 == other.participant1 and self.participant2 == other.participant2
        return False

    def __ne__(self, other):
        return self.participant1 != other.participant1 or self.participant2 != other.participant2

    def add_game(self, game):
        self.participant1.add_game(game)
        self.participant2.add_game(game)

    # Methods for Couple-to-Couple games
    def add_sets(self, n):
        self.participant1.add_sets(n)
        self.participant2.add_sets(n)

    def add_balls(self, n):
        self.participant1.add_balls(n)
        self.participant2.add_balls(n)


class Game:

    # Players can be either Participant or Couple instances
    player1 = None
    player2 = None
    date = None
    time = None
    results = None

    def __init__(self, player1, player2):
        if (isinstance(player1, Participant) and isinstance(player2, Participant)) or \
                (isinstance(player1, Couple) and isinstance(player2, Couple)):
            self.player1 = player1
            self.player2 = player2
            self.player1.add_game(self)
            self.player2.add_game(self)
        else:
            sys.exit("Error: Either players types are not supported, or they belong to different classes:\n" +
                     str(type(player1)) + "\n" + str(type(player2)))

    def __str__(self):
        return str(self.date) + " " + str(self.time) + "    " + str(self.player1) + "  vs.  " + str(self.player2)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.player1 == other.player1 and self.player2 == other.player2) or \
                   (self.player1 == other.player2 and self.player2 == other.player1)
        return False

    def __ne__(self, other):
        return (self.player1 != other.player1 or self.player2 != other.player2) and \
               (self.player1 != other.player2 or self.player2 != other.player1)

    def set_datetime(self, date, time):
        self.date = date
        self.time = time
        self.results = []

    def add_result(self, result):
        if len(self.results) == NUMBER_OF_SETS:
            return False

        self.results.append(result)
        if result[0] > result[1]:
            self.player1.add_sets(1)
        else:
            self.player2.add_sets(1)

        self.player1.add_balls(result[0] - result[1])
        self.player2.add_balls(result[1] - result[0])
        return True


class Day:

    date = None
    participants = None
    games = None

    def __init__(self, date):
        self.date = date
        self.participants = []
        self.games = []

    def __str__(self):
        return str(self.date)

    def add_game(self, game):
        if game in self.games:
            sys.exit("Error: The same game in one day: " + str(game))
        self.games.append(game)

        if isinstance(game.player1, Participant):
            self.participants.append(game.player1)
            self.participants.append(game.player2)
        else:
            self.participants.append(game.player1.participant1)
            self.participants.append(game.player1.participant2)
            self.participants.append(game.player2.participant1)
            self.participants.append(game.player2.participant2)


class DataBase:

    participants = None
    days = None

    def __init__(self):
        pass

    def save_participants(self, participants):
        self.participants = participants

    def save_days(self, days):
        self.days = days
