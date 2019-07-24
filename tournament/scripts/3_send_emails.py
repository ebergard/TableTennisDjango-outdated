# Run this script from APPLIEDTECH domain
# to send emails with schedules to the participants
# and forget about it!

import cPickle as pickle
from functions import *

with open(os.path.join(LOG_FOLDER, "data-pickled"), "rb") as fp:
    db = pickle.load(fp)

send_emails_with_schedule(db.participants)
