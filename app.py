import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# Get MongoDB URI from Render environment variable
MONGO_URI = os.environ.get("MONGO_URI")

if not MONGO_URI:
    raise Exception("MONGO_URI not found in environment variables")

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)

db = client["votingDB"]
votes = db["votes"]


# Home page
@app.route("/")
def index():
    return render_template("index.html")


# Vote submission
@app.route("/vote", methods=["POST"])
def vote():

    name = request.form.get("name")
    candidate = request.form.get("candidate")

    if not name or not candidate:
        return "Invalid vote data"

    # store vote in MongoDB
    votes.insert_one({
        "name": name,
        "candidate": candidate
    })

    return redirect(url_for("results"))


# Results page
@app.route("/results")
def results():

    results = {
        "Candidate A": votes.count_documents({"candidate": "Candidate A"}),
        "Candidate B": votes.count_documents({"candidate": "Candidate B"}),
        "Candidate C": votes.count_documents({"candidate": "Candidate C"})
    }

    return render_template("results.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)
