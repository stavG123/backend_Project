#project_routes.py
'''
   terminal commands: 
   cd venv
   Scripts/activate   
   $env:FLASK_APP = "project_routes.py" 
   $env:FLASK_DEBUG = "1"
   flask run
'''
import ProjectCSC341_1 as my_db
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=my_db.engine)
session = Session()

from project_form import Team_Form,Swimmer_Form

from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)

x_list=session.query(my_db.Team).all()
x_choices = []
for item in x_list:
   mylist=[]
   mylist.append(str(item.id))
   mylist.append("{}, {}".format(item.TeamName, item.CoachName) )
   my_tuple = tuple(mylist)
   x_choices.append(my_tuple)
print(x_choices)

app.config["SECRET_KEY"]='why_a_duck?'

@app.route("/")
def myredirect():
   return redirect(url_for('team'))

#insert a team
@app.route('/team', methods=['GET', 'POST'])
def team():
   form=Team_Form()
   if form.validate_on_submit():
      result = request.form
      a_team = my_db.Team(TeamName=result["team_name"], CoachName=result["coach_name"], Location=result["Location"])
      session.add(a_team)
      session.commit() 

      mylist=[]
      mylist.append(str(a_team.id))
      mylist.append("{}, {}".format(a_team.TeamName, a_team.CoachName))
      my_tuple = tuple(mylist)
      x_choices.append(my_tuple)
      return render_template('team_handler.html', title="Insert team from handler", header="Insert team Form handler", result=result)
   
   return render_template('team.html', title="Insert team Form", header="Insert team Form", form=form)   


from ProjectCSC341_1 import Swimmer
#insert a swimmer 
@app.route('/swimmer_form', methods=['GET', 'POST'])
def swimmer_form():
   form = Swimmer_Form()
   form.team_id.choices=x_choices
   print(form.validate_on_submit())
   if form.validate_on_submit():
      result = request.form
      a_swimmer = Swimmer(Name=result["swimmer_name"], Age=result["swimmer_age"], Gender=result["swimmer_gender"], Team_id=result["team_id"])

      a_swimmer.team_id=result["team_id"]
      session.add(a_swimmer)
      session.commit() 
      return render_template('swimmer_form_handler.html', title="Insert swimmer Form Handler", header="Insert swimmer Form handler", result=result)
   
   return render_template('swimmer_form.html', title="Insert swimmer Form", header="Insert swimmer Form", form=form)

#display--first table
import ProjectCSC341_1 as my_db
Session = sessionmaker(bind=my_db.engine)
session = Session()
query = session.query(my_db.Swimmer)
results = query.all()
print(results)
result_dict = [u.__dict__ for u in results]
print(result_dict)

@app.route('/first_table')
def planet_table():
   query=session.query(my_db.Swimmer)
   results=query.all()
   result_dict=[u.__dict__ for u in results]
   return render_template('first_table.html', title="first_table", header="first_table", Swimmer=result_dict)


@app.route('/second_datatable')
def planet_datatable():
   query=session.query(my_db.Swimmer)
   results=query.all()
   result_dict=[u.__dict__ for u in results]
   return render_template('second_datatable.html', title="second_datatable", header="second_datatable", Swimmer=result_dict)



@app.route('/third_table')
def Swimmer_dgridjs():
   query=session.query(my_db.Swimmer)
   results=query.all()
   result_dict=[u.__dict__ for u in results]
   columns = list(result_dict[0].keys())
   columns.remove('_sa_instance_state')
   print(columns)
   data = []
   for record in result_dict:
      rowList = list(record.values())
      rowList.pop(0)
      data.append(rowList)
   print(data)
   return render_template('third_table.html', 
                          title="third_table Data Table", 
                          header="third_table Data Table", columns=columns, data=data)




if __name__ == "__main__":
   app.run(debug=True) 