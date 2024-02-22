from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

debug = DebugToolbarExtension(app)

RESPONSES = []


@app.get('/')
def survey_start():
    title = survey.title
    instructions = survey.instructions

    return render_template('survey_start.html',
                           title=title,
                           instructions=instructions)
# @app.post('/begin')
# def redirect_to_question():


@app.post('/begin')
def redirect_to_questions():
    return redirect("/questions/0")


@app.get('/questions/<int:question_number>')
def show_question_form(question_number):

    question = survey.questions[question_number]

    return render_template(
        "question.html",
        question=question
    )

