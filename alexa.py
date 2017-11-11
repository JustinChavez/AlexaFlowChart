import logging
import os
from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


BeginState = "S1"

endStates = ["S4","S7","S9","S11"]

yesTrans = dict()
yesTrans["S1"] = "S3"
yesTrans["S2"] = "S4"
yesTrans["S3"] = "S5"
yesTrans["S5"] = "S7"
yesTrans["S6"] = "S8"
yesTrans["S8"] = "S9"
yesTrans["S10"] = "S11"


noTrans = dict()
noTrans["S1"] = "S2"
noTrans["S2"] = "S3"
noTrans["S3"] = "S6"
noTrans["S5"] = "S6"
noTrans["S6"] = "S8"
noTrans["S8"] = "S10"
noTrans["S10"] = "S11"





@ask.launch

def new_game():
    
    welcome_msg = render_template('welcome')
    session.attributes['state'] = BeginState
    session.attributes['help'] = False

    start = render_template(session.attributes['state'])

    return question(welcome_msg + " " + start)


@ask.intent("YesIntent")

def next_round():

    #if currently in help state
    if(session.attributes['help']):
        round_msg1 = render_template('continue')
        round_msg2 = render_template(session.attributes['state'])
        session.attributes['help'] = False
        return question(round_msg1 + " " + round_msg2)

    session.attributes['state'] = yesTrans[session.attributes['state']]
    
    if(session.attributes['state'] in endStates):
        #retrieve the specific end message for the specific state
        round_msg = render_template(session.attributes['state'])
        return statement(round_msg)
    else:
        round_msg = render_template(session.attributes['state'])
        return question(round_msg)

@ask.intent("NoIntent")
def next_round():
    if(session.attributes['help']):
        round_msg = render_template('helpno')
        return statement(round_msg)


    session.attributes['state'] = noTrans[session.attributes['state']]
    
    if(session.attributes['state'] in endStates):
        #retrieve the specific end message for the specific state
        round_msg = render_template(session.attributes['state'])
        return statement(round_msg)
    else:
        round_msg = render_template(session.attributes['state'])
        return question(round_msg)

@ask.intent("AMAZON.HelpIntent")

def next_round():

    session.attributes['help'] = True
    round_msg = render_template('help')
    return question(round_msg)

@ask.intent("AMAZON.StopIntent")
def next_round():
    round_msg = render_template('stop')
    return statement(round_msg)

@ask.intent("AMAZON.CancelIntent")
def next_round():
    round_msg = render_template('stop')
    return statement(round_msg)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
