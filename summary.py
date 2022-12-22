import html
import time

import openai
from openai.error import ServiceUnavailableError, APIError, Timeout

import settings

openai.api_key = settings.OPENAI_KEY

prompt = """\
Answer the question as truthfully as possible using the provided Search Results. Use this current date: {date}. Do not repeat text. Cite one relevant search result per sentence using [${index}]. Only cite results that were used to create the answer.  Use at most 150 words.

Format:
* Search Result [${index}]: `${search result text}`
 
Search Results:
""".replace("{date}", time.strftime("%A, %B %d, %Y", time.gmtime()))

prompt_question = """\
Q: `{query}`
A:"""

prompt_result = """\
* Search Result [{index}]: `{result}`
"""


def generate_prompt(query, chunks):
    question = prompt
    for i, chunk in enumerate(chunks):
        text = " ".join(chunk.text.split())
        question += prompt_result.format(index=i + 1, result=text)
    user_prompt = question + "\n" + prompt_question.format(query=query)
    return user_prompt


def replace_links(response, chunks):
    for i, chunk in enumerate(chunks):
        response = response.replace(f"[{i + 1}]", f"<a href='#result-{i + 1}'>[{i + 1}]</a>")
    return response


def get_summary(query, chunks):
    prompt = generate_prompt(query, chunks)
    try:
        response = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=0,
                                            max_tokens=settings.OPENAI_TOKEN_MAX)
        response = response.choices[0].text
    except (ServiceUnavailableError, APIError, Timeout):
        response = "Error generating summary"
    response = html.escape(response)
    response = replace_links(response, chunks)
    return response
