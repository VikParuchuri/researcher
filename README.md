# Snip Search

Snip search combines Google results and GPT-3 to give concise answers to search queries, with citations.

## Screenshots

| Games        | Recommendations |
|--------------|-----------------|
| ![Search 1](images/screen1.png) | ![Search 2](images/screen2.png)    |

## Example

Question: `What are alternatives to FastAPI?`

Response: ```FastAPI and Flask are two popular Python web frameworks used to build APIs and web applications. FastAPI is a full-stack framework that offers everything you need to build an API, while Flask is a micro framework that doesn't provide all the features that FastAPI does. FastAPI focuses on reliability, security, and simplicity, and is designed to build APIs easily and quickly. Flask is less well-documented and is slower than FastAPI, but is useful when you want to prototype an idea quickly or build a simple web application. [1] WSGI is a Python standard specifically written for web applications and servers to interface with each other, while ASGI was introduced by the inventors of FastAPI and is a specification to build event-driven, asynchronous web applications.```

# Installation

* Clone this repository
* Make sure you have Python 3.9+ installed
* `pip install -r requirements.txt`
* `python app.py`