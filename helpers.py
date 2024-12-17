from flask import Flask, redirect, render_template, request, session
from functools import wraps
import os

ARTICLES_DIR = "articles"

def login_required(func):
    # Decorate routes to require login
    @wraps(func)
    # To accept any arguments that might be passed to the original function
    def decorated_function(*args, **kwargs):
        if session.get("admin") is not True:
            return redirect("/login")
        return func(*args, **kwargs)
    return decorated_function


def error(message, code=400):
    # Render error message to user
    return render_template("error.html", top=code, bottom=message)


def generate_next_article_id():
    """
    Generates the next available article ID by checking existing files
    and finding the next largest number.
    """
    next_id = 1
    for filename in os.listdir(ARTICLES_DIR):
        if filename.startswith('article') and filename.endswith('.json'):
            try:
                # Extract the number from articleN.json
                article_id = int(filename[7:-5])  # Remove 'article' prefix and '.json' suffix
                if article_id >= next_id:
                    next_id = article_id + 1
            except ValueError:
                continue
    
    return next_id