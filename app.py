import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# ======================
# MongoDB Connection
# ======================
MONGO_URI = os.environ.get("MONGO_URI")

if not MONGO_URI:
    raise Exception("MONGO_URI not found")

client = MongoClient(MONGO_URI)

db = client["votingDB"]
votes = db["votes"]   # ✅ THIS LINE MUST EXIST


# ======================
# Routes
# ======================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/vote", methods=["POST"])
def vote():
    name = request.form.get("name")
    candidate = request.form.get("candidate")

    votes.insert_one({   # ← using votes here
        "name": name,
        "candidate": candidate
    })

    return redirect(url_for("results"))


@app.route("/results")
def results():
    a_votes = votes.count_documents({"candidate": "Candidate A"})
    b_votes = votes.count_documents({"candidate": "Candidate B"})
    c_votes = votes.count_documents({"candidate": "Candidate C"})

    total = a_votes + b_votes + c_votes
    if total == 0:
        total = 1

    return render_template(
        "result.html",
        a_votes=a_votes,
        b_votes=b_votes,
        c_votes=c_votes,
        a_percent=(a_votes / total) * 100,
        b_percent=(b_votes / total) * 100,
        c_percent=(c_votes / total) * 100
    )


if __name__ == "__main__":
    app.run(debug=True)

