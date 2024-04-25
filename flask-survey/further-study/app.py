from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

# key names will use to store some things in the session;
# put here as constants so we're guaranteed to be consistent in
# our spelling of these
RESPONSES_KEY = "responses"
CURRENT_SURVEY_KEY = "current_survey"

app = Flask(__name__)
app.config['SECRET_KEY'] = "Secrehjhdhiwhidw_hkhdiw"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route("/")
def select_survey():
    """Select a survey"""
    return render_template("select_survey.html", surveys = surveys)



@app.route("/", methods=["POST"])
def pick_survey():
    """Select a survey"""

    survey_id = request.form["survey_key"]
    survey = surveys[survey_id]
    session[CURRENT_SURVEY_KEY] = survey_id

    return render_template("survey_start.html", survey = survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses."""

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")


@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display current question."""
    responses = session.get(RESPONSES_KEY)
    survey_code =  session[CURRENT_SURVEY_KEY]
    survey = surveys[survey_code]

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != qid):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

   

    question = survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question, responses=responses)


@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    action = request.form.get("action")
    choice = request.form.get("answer")
    responses = session[RESPONSES_KEY]
    survey_code =  session[CURRENT_SURVEY_KEY]
    survey = surveys[survey_code]

   
    if action == "prev":
     if len(responses) == 0:
            # Handle case when there are no responses (e.g., redirect to the first question)
            return redirect(f"/questions/{len(responses)}")
     else:
            # Redirect to the previous question
            return redirect(f"/questions/{len(responses) - 1}")

    elif action == "skip":
     choice = ""
     responses.append(choice)
     session[RESPONSES_KEY] = responses
   
     if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")
     else:
        return redirect(f"/questions/{len(responses)}")
    elif action == "continue":
     
      if not choice:
       return redirect(f"/questions/{len(responses)}") 
      responses.append(choice)
      session[RESPONSES_KEY] = responses

      if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")
      else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""

    responses = session[RESPONSES_KEY]

    survey_code =  session[CURRENT_SURVEY_KEY]
    survey = surveys[survey_code]

    result_dict = dict(zip(survey.questions, responses))
    
    return render_template("completion.html", result_dict = result_dict)