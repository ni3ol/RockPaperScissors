from flask import Flask, request
from jinja2 import Environment, FileSystemLoader
import random

app = Flask(__name__)

environment = Environment(loader=FileSystemLoader("./"))

options = ['rock', 'paper', 'scissors']


def play(choice, random_choice, user_score, random_score):
    
    if choice == random_choice:
        return 'We tie!', user_score, random_score
    elif (
        (random_choice == 'rock' and choice == 'scissors') or
        (random_choice == 'paper' and choice == 'rock') or
        (random_choice == 'scissors' and choice == 'paper') 
    ):
        return 'I win!', user_score, random_score + 1
    else:
        return 'You win!', user_score + 1, random_score

@app.route("/", methods=["GET"])
def game():
    template = environment.get_template("index.html")
    if 'user_score' and 'random_score' not in request.args:
        user_score = 0
        random_score = 0
    else: 
        user_score = int(request.args['user_score'])
        random_score = int(request.args['random_score'])
    if 'choice' in request.args:
        choice = request.args['choice']
        random_choice = random.choice(options)
        outcome, user_score, random_score = play(choice, random_choice, user_score, random_score)
        return template.render(random_choice=random_choice, choice=choice, outcome=outcome, user_score=user_score, random_score=random_score)
    else:
        return template.render(user_score=user_score, random_score=random_score)

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()