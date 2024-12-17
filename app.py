from flask import Flask, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import json
import os

from helpers import login_required, error, generate_next_article_id

"""Initialize admin login database
Admin username and hashed password will be stored in a json file."""
admin_info = "admin.json"

"""Initialize the webapp"""
app = Flask(__name__)
app.secret_key = "my_micro_blog"

"""Get all the file in the articles folder in a string of text
then parse that text into dictionary type by using json.load"""
ARTICLES_DIR = "articles"

def load_articles():
    # Create an empty list to store articles
    articles = []
    # Loop through each file in the articles directory
    for filename in os.listdir(ARTICLES_DIR):
        # Open each file in reading mode
        with open(os.path.join(ARTICLES_DIR, filename), "r") as file:
            # Load json content and append into articles list
            articles.append(json.load(file))
    return articles


"""Home page that no need login"""
@app.route("/")
def index():
    articles = load_articles()
    if session.get["admin"]:
        return render_template("admin.html", articles=articles)
    else:
        return render_template("home.html", articles=articles)


"""Show article"""
# Create an URL route that captures a number from the URL and passes it to the function as article_id
@app.route("/article/<int:article_id>")
def show_article(article_id):
    # Show a specific article based on its ID. The ID is extracted from the filename (articleN.json)
    article_name = f"article{article_id}.json"
    filepath = os.path.join(ARTICLES_DIR, article_name)
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as file:
                article = json.load(file)
                return render_template("article.html", article=article)
        except json.JSONDecodeError:
            return error("Error reading article", 500)
    else:
        return error("Article not found", 404)


"""Dashboard that need admin login"""
@app.route("/admin")
@login_required
def admin():
    articles = load_articles()
    return render_template("admin.html", articles=articles)


"""New article"""
@app.route("/new", methods=["GET", "POST"])
@login_required
def new_article():
    now = datetime.now()
    if request.method == "POST":
        article_id = generate_next_article_id()
        new_name = f"article{article_id}.json"
        new_article = {
            "id": article_id,
            "title": request.form.get("title"),
            "date": now.strftime("%d/%b/%Y"),
            "content": request.form.get("content")
        }
        with open(os.path.join(ARTICLES_DIR, new_name), "w") as file:
            json.dump(new_article, file)
        return redirect("/admin")
    else:
        return render_template("new.html", now=now)


"""Edit article"""
@app.route("/edit/<int:article_id>", methods=["GET", "POST"])
@login_required
def edit_article(article_id):
    now = datetime.now()
    edit_article_name = f"article{article_id}.json"
    edit_filepath = os.path.join(ARTICLES_DIR, edit_article_name)
    if request.method == "POST":
        edit_article = {
            "id": article_id,
            "title": request.form.get("title"),
            "date": now.strftime("%d/%b/%Y"),
            "content": request.form.get("content")
        }
        with open(os.path.join(ARTICLES_DIR, edit_article_name), "w") as file:
            json.dump(edit_article, file)
        return redirect("/admin")
    # When access by GET request, the edit.html will show the content of the current article
    else:
        # Check if the article exist
        if os.path.exists(edit_filepath):
            with open(edit_filepath, "r") as file:
                article = json.load(file)
            return render_template(
                "edit.html", 
                id=article["id"], 
                title=article["title"], 
                content=article["content"], 
                now=now
            )
        else:
            return error("The article does not exist", 404)


"""Delete article"""
@app.route("/delete/<int:article_id>", methods=["POST"])
@login_required
def delete_article(article_id):
    delete_article_name = f"article{article_id}.json"
    delete_filepath = os.path.join(ARTICLES_DIR, delete_article_name)
    if os.path.exists(delete_filepath):
        os.remove(delete_filepath)
        return redirect("/admin")
    else:
        return error("The article does not exist", 404)


"""Login function"""
@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return error("Must input username", 400)

        if not request.form.get("password"):
            return error("Must input password", 400)

        # Load admin username and password from database
        if os.path.exists(admin_info):
            with open(admin_info, "r") as file:
                try:
                    admin = json.load(file)
                    if admin:
                        admin_username = admin["username"]
                        admin_password = admin["password"]
                except json.JSONDecodeError:
                    return error("Admin info is corrupted", 404)
        else:
            return error("Admin info does not exist", 404)

        # Check if username existed and password is valid
        username = request.form.get("username")
        password = request.form.get("password")

        if username == admin_username and check_password_hash(admin_password, password):
            session["admin"] = True
            return redirect("/admin")
        else:
            return render_template("error.html")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run()