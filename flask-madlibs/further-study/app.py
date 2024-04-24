from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from stories import stories


app = Flask(__name__)
app.config['SECRET_KEY'] = "Secrete-hkhdhihihi-iuiyyu"
debug = DebugToolbarExtension(app)

# @app.route("/")
# def ask_question():
#     """Show list of Story form"""
#     return render_template('questions.html', prompts = story.prompts)


 
@app.route("/")
def select_story():
    """Show list of story to choose from"""
    return render_template('select_story.html', stories = stories.values())

@app.route("/questions")
def ask_question():
    """Show list of Story form"""
    story_id = request.args["story_id"]
    story = stories[story_id]
    prompts = story.prompts

    return render_template('questions.html', story_id=story_id, title=story.title, prompts = prompts)

@app.route("/story")
def show_story():
   """Show story result."""
   story_id = request.args["story_id"]
   story = stories[story_id]
   text = story.generate(request.args)
   return render_template('story.html',title=story.title, text=text)