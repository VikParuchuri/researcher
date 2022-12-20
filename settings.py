RESULT_COUNT = 10
MIN_RESULTS = 5
LANGUAGE = "en"
CHUNK_MAX_LENGTH = 256
MAX_PROCESSES = 5
MAX_TRACKER_URLS = 5

import os
if os.path.exists("private.py"):
    from private import *