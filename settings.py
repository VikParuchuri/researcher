RESULT_COUNT = 15
MIN_RESULTS = 5
LANGUAGE = "en"
CHUNK_MAX_LENGTH = 512
CHUNK_LIMIT = 5
MAX_PROCESSES = 10
MAX_TRACKER_URLS = 3
MAX_SCRIPTS = 15

import os
if os.path.exists("private.py"):
    from private import *