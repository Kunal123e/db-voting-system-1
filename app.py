import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# ======================
# MongoDB Connection
# ======================
MONGO_URI = os.environ.get("MONGO_URI")

if not MONGO_URI:
    raise Exception("MONGO_URI not found in environment variables")

try:
    client = MongoClient(MONGO_URI)
    db = client["votingDB"]
    votes = db["votes"]
    print("MongoDB Connected")
except Exception as e:
    print("MongoDB Connection Error:", e)


# ======================
# Routes
# ======================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/vote", methods=["POST"])
def vote():
    try:
        name = request.form.get("name")
        candidate = request.form.get("candidate")

        if not name or not candidate:
            return "Missing data", 400

        votes.insert_one({
            "name": name,
            "candidate": candidate
        })

        return redirect(url_for("results"))

    except Exception as e:
        return f"Error: {str(e)}", 500


@app.route("/results")
def results():
    try:
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

    except Exception as e:
        return f"Error loading results: {str(e)}", 500


# ======================
# Run App
# ======================
if __name__ == "__main__":
    app.run(debug=True)
