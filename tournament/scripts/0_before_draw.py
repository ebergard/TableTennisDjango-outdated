# Run this script before a draw and then forget about it!
# Result:
# 1. shedule with ids
# 2. pickled data


import pickle
from tournament.scripts.functions import *
from tournament.scripts.classes import DataBase
from tournament.scripts.constants import *


# Clear logs
for the_file in os.listdir(LOG_FOLDER):
    file_path = os.path.join(LOG_FOLDER, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        logger.debug(e)

# Generate new schedule
schedule_ready = False
while not schedule_ready:
    games, games_per_player, participants = generate_games()
    schedule_ready, max_games_per_day, days = generate_schedule(games)

print("Games number = " + str(len(games)))
print("Games per person = " + str(games_per_player))
print("Maximum number of games per day = " + str(max_games_per_day))
write_games_to_xl(participants)

if not SINGLE:
    logger.debug("Number of duplicate rivals for each player:\n")
    for p in participants:
        logger.debug(str(p) + ": " + str(p.duplicate_rivals()) + "\n")

db = DataBase()
db.save_participants(participants)
db.save_days(days)

with open(os.path.join(LOG_FOLDER, "data-pickled"), "wb") as fp:
    pickle.dump(db, fp)
