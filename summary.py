prompt = """\
Instructions: 
# Generate a comprehensive and informative answer (but no more than 150 words) for a given question solely based on the provided web Search Results (URL and Summary).
# You must only use information from the provided search results. Use an unbiased and journalistic tone.
# Combine search results together into a coherent answer. Do not repeat text.
# Cite search results using [${index}]. Cite one search result per sentence. Only cite the most relevant results that answer the question accurately.
# If different results refer to different entities with the same name, write separate answers for each entity.
# Format:
# Question: `${question text}`
# Search result [${index}]: `${search result text}`
Answer:"""

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
