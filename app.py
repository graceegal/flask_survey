from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# RESPONSES = []
# 0123


@app.get('/')
def survey_start():
    ''''''
    session["responses"] = []

    title = survey.title
    instructions = survey.instructions
    # RESPONSES.clear()

    return render_template('survey_start.html',
                           title=title,
                           instructions=instructions)


@app.post('/begin')
def redirect_to_questions():
    ''''''

    return redirect("/questions/0")


@app.get('/questions/<int:question_number>')
def show_question_form(question_number):
    ''''''

    question = survey.questions[question_number]

    return render_template(
        "question.html",
        question=question
    )


@app.post('/answer')
def store_answer():
    ''''''

    answer = request.form.get('answer')
    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses
    # RESPONSES.append(answer)
    # print('responses', RESPONSES)

    question_number = len(session["responses"])
    if question_number < len(survey.questions):
        return redirect(f'/questions/{question_number}')

    return redirect('/thank_you')


@app.get('/thank_you')
def redirect_thank_you():
    ''''''

    questions = survey.questions

    breakpoint()

    return render_template(
        'completion.html',
        responses = session["responses"],
        questions = questions
    )
