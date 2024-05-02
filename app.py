from flask import Flask, render_template, jsonify, request
import numpy as np

app = Flask(__name__)

# Define constants
EMPTY = 0
PLAYER_1 = 1
PLAYER_2 = 2
ROW_COUNT = 6
COLUMN_COUNT = 7
WINNING_LENGTH = 4

# Front-end route
@app.route('/')
def index():
    return render_template('connect4.html')

if __name__ == "__main__":
    app.run(debug=True)
