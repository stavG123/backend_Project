#project_form.py
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField
from wtforms.validators import InputRequired, Length

#insert to PK(team table)
####################################################
class Team_Form(FlaskForm):
   
   team_name=StringField("Team Name", 
   validators=[InputRequired(message="You must enter a info"), 
   Length(min=1, max=60, message="info length must be between 2 and 60 characters")])

   coach_name=StringField("Coach Name", 
   validators=[InputRequired(message="You must enter a info"), 
   Length(min=1, max=60, message="info length must be between 2 and 60 characters")])

   Location=StringField("Location ", 
   validators=[InputRequired(message="You must enter a info"), 
   Length(min=1, max=60, message="info length must be between 2 and 60 characters")])

   submit = SubmitField("Insert Team")
#insert to Fk(swimmer table)
#####################################################

class Swimmer_Form(FlaskForm):
   
   swimmer_name=StringField("Swimmer Name", 
   validators=[InputRequired(message="You must enter a info"), 
   Length(min=1, max=60, message="info length must be between 2 and 60 characters")])

   swimmer_age=StringField("Swimmer Age", 
   validators=[InputRequired(message="You must enter a info"), 
   Length(min=1, max=60, message="info length must be between 2 and 60 characters")])

   swimmer_gender=StringField("swimmer gender", 
   validators=[InputRequired(message="You must enter a info"), 
   Length(min=1, max=60, message="info length must be between 2 and 60 characters")])

   team_id = SelectField("Team ID ")

   submit = SubmitField("Insert swimmer")