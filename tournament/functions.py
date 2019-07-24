import sys
import datetime
import random
from datetime import *
from time import *
from itertools import cycle
from tournament.models import Tournament, Game
from django.utils import timezone


def get_current_tournament():
    if Tournament.objects.exists():
        return Tournament.objects.latest('id')
    return None


def get_tournament_status(tournament):
    if tournament:
        # Registration is open
        if timezone.now() < tournament.reg_end:
            return 0
        # Registration is over
        elif timezone.now() >= tournament.reg_end and timezone.localdate() < tournament.start_date:
            return 1
        # Tournament started
        elif tournament.start_date <= timezone.localdate() <= tournament.end_date:
            return 2
        # Tournament finished
        else:
            return 3
    return 4


# Get the current tournament
tournament = get_current_tournament()

try:
    # SINGLE = True for Single-to-Single games,
    # SINGLE = False for Couple-to-Couple games
    SINGLE = tournament.single

    # Number of participants
    NUMBER_OF_PARTICIPANTS = tournament.number_of_participants()

    # Number of sets in one game
    NUMBER_OF_SETS = tournament.number_of_sets

    # Schedule parameters
    #NUMBER_OF_DAYS = tournament.start_date_playoff.days - tournament.start_date.days
    #START_DAY = tournament.start_date
    START_TIME = tournament.game_start_time
    TIME_INTERVAL = tournament.game_duration
except:
    pass


def get_number_of_rounds():

    if NUMBER_OF_PARTICIPANTS % 2 == 0:
        return 10
    else:
        return 5


def generate_games_subset(games, participants):

    random.shuffle(participants)
    number_of_participants = len(participants)
    games_subset = []

    for i in range(number_of_participants // 2):

        game = Game(tournament=tournament, id1=participants[i], id2=participants[number_of_participants - i - 1])

        if game not in games:
            games_subset.append(game)

    return games_subset


def number_of_games(games, p_id):
    number = 0
    for game in games:
        if game.id1 == p_id or game.id2 == p_id:
            number += 1
    return number


def games_per_person(games, participants):

    games_per_person_list = [number_of_games(games, p) for p in participants]
    return games_per_person_list


def games_number_is_equal(games, participants):

    if len(set(games_per_person(games, participants))) == 1:
        return True
    else:
        return False


def generate_games():
    tour = get_current_tournament()
    games_number = tour.games_per_person
    participants = [i for i in range(1, tour.number_of_participants() + 1)]

    games = []
    games_per_person_list = [0] * len(participants)
    step = 1

    for p in cycle(participants):
        p2 = p + step
        if p2 > len(participants):
            p2 -= len(participants)
        game = Game(tournament=tour, id1=p, id2=p2) if p < p2 else Game(tournament=tour, id1=p2, id2=p)
        if game not in games:
            games.append(game)
            games_per_person_list[p - 1] += 1
            games_per_person_list[p2 - 1] += 1
        else:
            step += 1

        if len(set(games_per_person_list)) == 1 and games_per_person_list[0] == games_number:
            break

    return games


def get_time(start_time):
    # return str(datetime.strptime(start_time, '%H:%M') + timedelta(minutes=TIME_INTERVAL))[11:-3]
    t = datetime.combine(datetime(1,1,1), start_time) + TIME_INTERVAL
    return t.time()


def get_dates():
    START_DAY = tournament.start_date
    NUMBER_OF_DAYS = tournament.start_date_playoff - tournament.start_date
    NUMBER_OF_DAYS = NUMBER_OF_DAYS.days
    days = []

    i = 0
    day = START_DAY
    while i < NUMBER_OF_DAYS:

        i += 1
        day_str = day.strftime("%a")

        if "Sun" in day_str or "Sat" in day_str:
            day = day + timedelta(days=1)
            continue
        days.append(day)
        day = day + timedelta(days=1)

    return days


def players_this_day(games, day):
    participants = []
    for game in games:
        if game.game_date == day:
            participants.append(game.id1)
            participants.append(game.id2)

    return participants


def have_slot_for_game(games, game, day, max_games):

    players = [game.id1, game.id2]

    for player in players:
        if players_this_day(games, day).count(player) >= max_games:
            return False
    return True


def games_this_day(games_all, day):
    games = []
    for game in games_all:
        if game.game_date == day:
            games.append(game)

    return games


def last_game_time(games_all, day):
    games = games_this_day(games_all, day)
    try:
        games.sort(key=lambda g: datetime.combine(datetime(1,1,1), g.start_time))
    except:
        pass
    return games[-1].start_time


def initial_games_number(days_number):
    t = get_current_tournament()
    nop = t.number_of_participants()
    gpp = t.games_per_person
    if gpp % days_number == 0 and nop % 2 == 0:
        return gpp // days_number
    return gpp // days_number + 1


def generate_schedule(games):

    days = get_dates()
    num_of_days = len(days)

    max_games_per_day = len(games) // num_of_days
    if len(games) % num_of_days != 0:
        max_games_per_day += 1

    not_set_games = []
    max_games = initial_games_number(num_of_days)
    max_attempts = 100
    attempt = 0

    while True:
        for game in games:
            for i in range(num_of_days):
                if len(players_this_day(games, days[i])) < max_games_per_day * 2:
                    if have_slot_for_game(games, game, days[i], max_games):
                        if len(games_this_day(games, days[i])) == 0:
                            game_time = START_TIME
                        else:
                            game_time = get_time(last_game_time(games, days[i]))

                        game.start_time = game_time
                        game.game_date = days[i]
                        break
                if i == num_of_days - 1:
                    not_set_games.append(game)

        if len(not_set_games) == 0:
            for game in games:
                game.save()
            print("Schedule generated with max games per person per day: {}".format(max_games))
            return
        else:
            attempt += 1
            if attempt == max_attempts:
                max_games += 1
                attempt = 0
            for game in games:
                game.start_time = None
                game.game_date = None
            random.shuffle(games)
            not_set_games = []
