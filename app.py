import os
from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# Get MongoDB connection from environment variable
MONGO_URI = os.environ.get("MONGO_URI")

# Connect to MongoDB
client = MongoClient(MONGO_URI)

db = client["votingDB"]
votes = db["votes"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/vote", methods=["POST"])
def vote():

    name = request.form.get("name")
    candidate = request.form.get("candidate")

    votes.insert_one({
        "name": name,
        "candidate": candidate
    })

    return "Vote Submitted Successfully"


@app.route("/results")
def results():

    a_votes = votes.count_documents({"candidate": "Candidate A"})
    b_votes = votes.count_documents({"candidate": "Candidate B"})
    c_votes = votes.count_documents({"candidate": "Candidate C"})

    total = a_votes + b_votes + c_votes

    if total == 0:
        total = 1

    a_percent = (a_votes / total) * 100
    b_percent = (b_votes / total) * 100
    c_percent = (c_votes / total) * 100

    return render_template(
        "result.html",
        a_votes=a_votes,
        b_votes=b_votes,
        c_votes=c_votes,
        a_percent=a_percent,
        b_percent=b_percent,
        c_percent=c_percent
    )


if __name__ == "__main__":
    app.run()
