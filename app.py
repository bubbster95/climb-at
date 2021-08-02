from flask import Flask, render_template, request
# from helpers import
import json

app = Flask(__name__)


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("index.html")
