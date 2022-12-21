## API
# Key to access the OpenAI API
OPENAI_KEY = ""
# Maximum number of tokens
OPENAI_TOKEN_MAX = 256

## Search
# Minimum length for valid search query
QUERY_MIN_LENGTH = 10
# Number of results to search for
RESULT_COUNT = 10
# Minimum number of valid search results
MIN_RESULTS = 5
# Maximum processes to use when scraping results
MAX_PROCESSES = 10

## Filtering
# Maximum number of tracker URLs allowed in a site (rejects sites with more)
MAX_TRACKER_URLS = 3

## Parsing
# Language to use to parse results
LANGUAGE = "en"
# Maximum length in words for context chunks to be used in prompt
CHUNK_MAX_LENGTH = 256
# Minimum length in words for context chunks to be used in prompt
CHUNK_MIN_LENGTH = 128
# Number of chunks to use when generating prompt
CHUNK_LIMIT = 6

## Display
# Maximum number of characters in a chunk to display
CHUNK_DISPLAY_CHARS = 500

import os

if os.path.exists("private.py"):
    pass
