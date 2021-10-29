from flask import Flask, render_template, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "password"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def start_game():
    """populates boggle board and saves the current board in session"""

    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get('highscore', 0)
    num_plays = session.get('num_plays', 0)

    return render_template('start.html', board = board, highscore = highscore, num_plays = num_plays)

@app.route('/process', methods=['POST'])
def process_guess():
    """checks if user submitted guess is valid"""

    guess = request.form['guess']
    guess_length = len(guess)

    result =  boggle_game.check_valid_word(session['board'], guess)
    
    return jsonify({'result' : result, 'guess_length' : guess_length, 'guess' : guess})

@app.route('/score', methods=['POST'])
def post_score():
    """updates user's final score and number of plays"""
    score = request.json['score']
    highscore = session.get('highscore', 0)
    num_plays = session.get('num_plays', 0)

    session['highscore'] = max(score, highscore)
    session['num_plays'] = num_plays + 1

    return jsonify(brokeRecord = score > highscore)


