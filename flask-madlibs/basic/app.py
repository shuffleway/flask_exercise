from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from stories import story


app = Flask(__name__)
app.config['SECRET_KEY'] = "Secrete-hkhdhihihi-key"
debug = DebugToolbarExtension(app)

@app.route("/")
def ask_question():
    """Show list of Story form"""
    return render_template('questions.html', prompts = story.prompts)

@app.route("/story")
def show_story():
   """Show story result."""
   text = story.generate(request.args)
   return render_template('story.html', text=text)
 