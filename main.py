from flask import Flask, render_template, Blueprint, redirect, request
from ebay_api import search_items

app = Flask(__name__)


@app.route("/")
@app.route("/home")
@app.route("/homepage")
def home():
    def_items = search_items(request.args.get('search') or 'furniture')
    return render_template("home.html", def_items=def_items)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/help")
def helper():
    return render_template("help.html")


if __name__ == '__main__':
    app.run(debug=True)
