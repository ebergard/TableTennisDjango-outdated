from itertools import cycle
from pprint import pprint


participants = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
games_number = 10
games_per_person = [0] * len(participants)

games = []
step = 1
for p in cycle(participants):
    p2 = p + step
    if p2 > len(participants):
        p2 -= len(participants)
    game = (p, p2) if p < p2 else (p2, p)
    if game not in games:
        games.append(game)
        games_per_person[game[0] - 1] += 1
        games_per_person[game[1] - 1] += 1
    else:
        step += 1

    if len(set(games_per_person)) == 1 and games_per_person[0] == games_number:
        break


print(games_per_person)
print("games number: {}".format(len(games)))
pprint(games)
