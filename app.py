import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# =======================
# MongoDB Connection
# =======================
MONGO_URI = os.environ.get("MONGO_URI")

if not MONGO_URI:
    raise Exception("❌ MONGO_URI not found. Set it in Render environment variables.")

try:
    client = MongoClient(MONGO_URI)
    db = client["votingDB"]
    votes = db["votes"]
    print("✅ MongoDB Connected Successfully")
except Exception as e:
    print("❌ MongoDB Connection Failed:", e)


# =======================
# Routes
# =======================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/vote", methods=["POST"])
def vo
