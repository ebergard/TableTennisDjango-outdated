# Run this script every time when games results are updated in schedule.xlsx

import cPickle as pickle
from functions import *

with open(os.path.join(LOG_FOLDER, "data-pickled"), "rb") as fp:
    db = pickle.load(fp)

load_results(db.days)
write_rating_to_xl(db.participants)

with open(os.path.join(LOG_FOLDER, "data-pickled"), "wb") as fp:
    pickle.dump(db, fp)
