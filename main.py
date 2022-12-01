# ---------------------------------------------------Import Modules----------------------------------------------------#
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditor
import requests

# ------------------------------------------------------CONSTANTS & Variables------------------------------------------#
# You will have to go to OWLBOT to get your own token
OWLBOT_API_TOKEN = "USE YOUR OWN API TOKEN THAT YOU GET OFF THEIR WEBSITE"
# This will not change.
owlbot_endpoint = f"https://owlbot.info/api/v4/dictionary/"

# ---------------------------------------------------------APP---------------------------------------------------------#
# Create app object from Flask Class
app = Flask(__name__)

# Configure the app object with a secret key. It can be whatever you want.
app.config['SECRET_KEY'] = 'THISISYOURSECRETKEYCOMEUPWITHSOMETHINGGREAT'

# Create object from CKEditor.
ckeditor = CKEditor(app)

# Specify that Bootstrap shall be utilized with app object
Bootstrap(app)


# ---------------------------------------------------------CLASSES-----------------------------------------------------#
# Create Class for a simple form with WTForms
class WordForm(FlaskForm):
    word = StringField("What word are you looking for?", validators=[DataRequired()])
    submit = SubmitField("Enter")


# ---------------------------------------------------------ROUTES------------------------------------------------------#
# Set home page routing
@app.route("/", methods=["GET", "POST"])
def look_up_word():
    # Create form object from WordForm Class
    form = WordForm()
    # If statement for when the "Enter" button on the form is clicked
    if form.validate_on_submit():
        word_lookup = form.word.data  # Pull the word from the form as a string
        url_endpoint = owlbot_endpoint + word_lookup.strip()  # Create endpoint to send to API
        headers = {"Authorization": f"Token {OWLBOT_API_TOKEN}"}  # Headers to send to API
        response = requests.get(url=url_endpoint, headers=headers)  # Get request to API for data
        response.raise_for_status()  # Raise a response in case information is incorrect
        data = response.json()  # Returned data from API in json format
        definition_list = data["definitions"]  # Get a list of all the definitions for the word
        # Returns index.html page from templates folder with the definitions of the word
        return render_template("index.html", definition_list=definition_list, word=word_lookup, form=form)
    return render_template("index.html", form=form)  # Returns index.html page from templates folder


# Initiate the script and start a development server
if __name__ == "__main__":
    app.run(debug=True)


