## API
# Key to access the OpenAI API
OPENAI_KEY = ""

## Search
# Minimum length for valid search query
QUERY_MIN_LENGTH = 10
# Number of results to search for
RESULT_COUNT = 15
# Minimum number of valid search results
MIN_RESULTS = 5
# Maximum processes to use when scraping results
MAX_PROCESSES = 10

## Filtering
# Maximum number of tracker URLs allowed in a site (rejects sites with more)
MAX_TRACKER_URLS = 3
# Maximum script tags to allow on a site (rejects sites with more)
MAX_SCRIPTS = 15

## Parsing
# Language to use to parse results
LANGUAGE = "en"
# Maximum length in words for context chunks to be used in prompt
CHUNK_MAX_LENGTH = 512
# Number of chunks to use when generating prompt
CHUNK_LIMIT = 5

## Display
# Maximum number of characters in a chunk to display
CHUNK_DISPLAY_CHARS = 500

import os
if os.path.exists("private.py"):
    from private import *