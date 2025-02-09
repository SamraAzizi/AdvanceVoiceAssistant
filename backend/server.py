import os
from livekit import api
from flask import Flask, request
from dotenv import load_dotenv
from flask_cors import CORS
from livekit.api import LiveKitApi, ListRoomsRequest
import uuid

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins" : "*"}})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)