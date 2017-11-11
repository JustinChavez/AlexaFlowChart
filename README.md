# Intro

In this tutorial I will be teaching how to make a Yes/No Framework as an Amazon Alexa skill.

I will demonstrate by building one of my favorite flowcharts from PHD Comics:

![alt text](https://raw.githubusercontent.com/JustinChavez/Flask-Ask-HW/master/tutorial/images/phd01.png "From PHD Comics")

Reference: http://www.phdcomics.com/comics.php?f=1632

(Note: I will be adding slight adjustments to the logic flow since not all answers are Yes/No in the comic.)

# Setup

We will be using the Python framework [Flask-Ask](https://github.com/johnwheeler/flask-ask) for this tutorial. Please follow [this quick introduction](https://developer.amazon.com/blogs/post/Tx14R0IYYGH3SKT/Flask-Ask-A-New-Python-Framework-for-Rapid-Alexa-Skills-Kit-Development) to the framework to get your development environment setup.

With your development environment set we can now move on 

# Build the Framework
First before you start you should have the framework you want to build into the Alexa skill ready. Just make sure that there is only one state that your logic flow starts with and only Yes/No answers to each question.

Next take your flowchart and label each question and ending statement with a number for reference to its state. For my flowchart I labeled each state with S1-11:

![alt text](https://raw.githubusercontent.com/JustinChavez/Flask-Ask-HW/master/tutorial/images/phd02.png "Adjusted from PHD Comics")

Now in your Python file, set a variable BeginState to reference the state that your framework begins on. For mine that would be state S1:

```Python
BeginState = "S1"
```
Next create a variable named endStates where you list the states that ends the framework:

```Python
endStates = ["S4","S7","S9","S11"]
```
We now need can direct the logic flow. We will create two dictionaries where the key is the current state and the value will be the next state to go to based on the answer Yes/No. 

```Python
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
```
For example, in my flowchart state S1 when given the answer yes moves to state S3. Thus I create in the yesTrans dictionary the key S1 has the value S3.

Now lets update our templates.yaml file to contain the correct phrases at each state. The key should be the state name and the value is the question or statment the state represents. Here is mine:

```
S1: Do you actually HAVE a question?

S2: Are you tring to show off?

S3: Are you sure it's not a dumb question or that the speaker already answered it?

S4: Go for it.

S5: Are you trying to show off?

S6: Do you really need to ask the question in public or could you follow up with him/her later?

S7: Proceed with caution.

S8: Are you the seminar organizer asking a question because no one else is and the awkward silence is making everyone uncomfortable?

S9: Thank God. Please ask the question and let's get out of here!

S10: Ok, you have a legitimate question. Do you actually care about the answer?

S11: FINE, ASK YOUR QUESTION.
```

# Build the intents
We can now move on to building the logic in the intents. 

Adjust the new_game function so that it will start on the indicated BeginState.

```Python
def new_game():
    
    welcome_msg = render_template('welcome')
    session.attributes['state'] = BeginState
    start = render_template(session.attributes['state'])

    return question(welcome_msg + " " + start)
```
Now we can adjust the YesIntent to read from the yesTrans dictionary to switch to the next state and ask its question. The code also detects if the current state is one of the indicated endStates. If so it will read its statement and end the session. 

```Python
@ask.intent("YesIntent")

def next_round():

    session.attributes['state'] = yesTrans[session.attributes['state']]
    
    if(session.attributes['state'] in endStates):
        #retrieve the specific end message for the specific state
        round_msg = render_template(session.attributes['state'])
        return statement(round_msg)
    else:
        round_msg = render_template(session.attributes['state'])
        return question(round_msg)
```
Now create the No intent. It is almost an exact copy of the Yes Intent.

```Python
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
```
# Conclusion
And that is all the code you need! Feel free to reference my code in alexa.py and templates.yaml. There I included a couple more intents to add help, stop, and cancel. Those intents are not needed for functionality, but are needed if you intend to publish to the Amazon store.

Hope this helps!

Justin
