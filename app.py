from flask import Flask, request, render_template, redirect, flash, session
from flask import flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# RESPONSES = []
# 0123


@app.get('/')
def show_survey_start():
    ''''''

    title = survey.title
    instructions = survey.instructions

    return render_template(
        'survey_start.html',
        title=title,
        instructions=instructions
    )


@app.post('/begin')
def start_survey():
    ''''''

    session["responses"] = []

    return redirect("/questions/0")


@app.get('/questions/<int:question_number>')
def show_question_form(question_number):
    ''''''
    questions_answered = len(session["responses"])

    if questions_answered == len(survey.questions):
        flash("Thank you! You have already completed the survey.")
        return redirect('/complete')
    elif questions_answered != question_number:
        flash("Sorry, you are trying to access an invalid question. Please"
              + " choose a valid response to continue.")
        return redirect(f'/questions/{questions_answered}')

    question = survey.questions[question_number]
    return render_template(
        "question.html",
        question=question
    )


@app.post('/answer')
def handle_question():
    ''''''

    answer = request.form.get('answer')

    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses

    if len(responses) < len(survey.questions):
        return redirect(f'/questions/{len(responses)}')

    return redirect('/complete')


@app.get('/complete')
def show_completion_page():
    ''''''
    responses = session["responses"]
    questions = survey.questions

    return render_template(
        'completion.html',
        responses=responses,
        questions=questions
    )
