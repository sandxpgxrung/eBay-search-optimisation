from flask import Flask, render_template, Blueprint, redirect, request
from ebay_api import search_items

app = Flask(__name__)


@app.route("/")
@app.route("/home")
@app.route("/homepage")
def home():
    items = search_items(request.args.get('search') or 'furniture')
    return render_template("home.html", items=items)


@app.route("/basket")
def basket():
    return render_template("basket.html")


@app.route("/login")
def login():
    return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)
