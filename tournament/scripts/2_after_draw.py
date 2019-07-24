# -*- coding: utf-8 -*-
# Run this script after a draw to identify participants and forget about it!
# Result:
# 1. shedule with names
# 2. updated pickled data

import cPickle as pickle
from functions import *

with open(os.path.join(LOG_FOLDER, "data-pickled"), "rb") as fp:
    db = pickle.load(fp)

if SINGLE:
    sheetname = "личное первенство"
else:
    sheetname = "парный турнир"

identify_participants(db.participants, sheetname)
write_schedule_to_xl(db.days, sheetname="Расписание")

with open(os.path.join(LOG_FOLDER, "data-pickled"), "wb") as fp:
    pickle.dump(db, fp)
