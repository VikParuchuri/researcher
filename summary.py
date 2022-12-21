import html

import openai
from openai.error import ServiceUnavailableError, APIError, Timeout
import settings
import time

openai.api_key = settings.OPENAI_KEY

prompt = """\
Instructions: 
# Generate a comprehensive and informative answer (but no more than 100 words) for a given question solely based on the provided web Search Results (URL and Summary).
# You must only use information from the provided search results. Use an unbiased and journalistic tone.
# Use this current date: {date}
# Combine search results together into a coherent answer. Do not repeat text.
# Cite one search result per sentence using [${index}]. Only cite the most relevant results that answer the question accurately.
# Format:
# Question: `${question text}`
# Search result [${index}]: `${search result text}`
Answer:""".replace("{date}", time.strftime("%A, %B %d, %Y", time.gmtime()))

prompt_question = """\
Question: `{query}`
"""

prompt_result = """\
Search result [{index}]: `{result}`
"""

def generate_prompt(query, chunks):
    question = prompt_question.format(query=query)
    for i, chunk in enumerate(chunks):
        text = " ".join(chunk.text.split())
        question += "\n" + prompt_result.format(index=i+1, result=text)
    user_prompt = question + "\n" + prompt
    return user_prompt

def replace_links(response, chunks):
    for i, chunk in enumerate(chunks):
        response = response.replace(f"[{i+1}]", f"<a href='#result-{i+1}'>[{i+1}]</a>")
    return response


def get_summary(query, chunks):
    prompt = generate_prompt(query, chunks)
    try:
        response = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=0, max_tokens=settings.OPENAI_TOKEN_MAX)
        response = response.choices[0].text
    except (ServiceUnavailableError, APIError, Timeout):
        response = "Error generating summary"
    response = html.escape(response)
    response = replace_links(response, chunks)
    return response
