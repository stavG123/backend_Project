#ProjectCSC341_1.py
from flask import sessions
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///project.db')
Base = declarative_base()

#the connection between the brifge tables
write_table = Table('write_table', Base.metadata,
    Column('Swimmer_id', Integer, ForeignKey('Swimmer.id')),
    Column('Event_id', Integer, ForeignKey('Event.id'))
)
#team table
class Team(Base):
    __tablename__ = 'Team'

    id=Column(Integer, primary_key=True)
    TeamName=Column(String)
    CoachName=Column(String)
    Location=Column(String)
    x=relationship("Swimmer")


#swimmer table
class Swimmer(Base):
    __tablename__ = 'Swimmer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String)
    Age = Column(Integer)
    Gender=Column(String)
    Team_id = Column(Integer, ForeignKey('Team.id'))
    written_by = relationship("Event", secondary=write_table, viewonly=True)

#event table
class Event(Base):
    __tablename__='Event'

    id=Column(Integer, primary_key=True)
    EventName=Column(String)
    Distance=Column(String)
    wrote = relationship("Swimmer", secondary=write_table, viewonly=True)

# Drop tables
Team.__table__.drop(engine, checkfirst=True)
Swimmer.__table__.drop(engine, checkfirst=True)
Event.__table__.drop(engine, checkfirst=True)
write_table.drop(engine, checkfirst=True)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

import os 
os.chdir(os.path.dirname(os.path.realpath(__file__)))

#open the txt file insert the swimming events 
with open("static/data/ProjectCSC341.txt","r") as f:
    for line in f:
        if line.strip():
            x=line.rstrip().split(",")
            y=Event(id=x[0],EventName=x[1],Distance=x[2])
            session.add(y)
session.commit()
session.flush()

#open the json file insert the swimmer info and the team info
import json

with open("static/data/Project.json", "r") as json_file:
    team_data = json.load(json_file)

for team_info in team_data:
    team = Team(
        TeamName=team_info["TeamName"],
        CoachName=team_info["CoachName"],
        Location=team_info["Location"]
    )

    session.add(team)
    session.commit()  

    for swimmer_info in team_info["Swimmers"]:
        swimmer = Swimmer(
            id=swimmer_info["id"],
            Name=swimmer_info["Name"],
            Age=swimmer_info["Age"],
            Gender=swimmer_info["Gender"],
            Team_id=team.id  
        )
        session.add(swimmer)

session.commit()
session.flush()


#insert to the bridge table info 
#stav swimmer 
session.execute(write_table.insert().values([(1,4),(1,5),(1,6)]))
session.commit()

#tarik swimmer 
session.execute(write_table.insert().values([(2,10),(2,11),(2,12)]))
session.commit()

#iris swimmer
session.execute(write_table.insert().values([(3,1),(3,2)]))
session.commit()

#michel andrew
session.execute(write_table.insert().values([(4,1),(4,2),(4,10)]))
session.commit()
#blum
session.execute(write_table.insert().values([(5,1)]))
session.commit()
#ledeckey
session.execute(write_table.insert().values([(6,3),(6,9)]))
session.commit()

#dispaly the results of the bridge table (swimmer to event):

swimmers = session.query(Swimmer)
for swimmer in swimmers:
    print("{} is swimming ".format(swimmer.Name))
    for event in swimmer.written_by:
        print(event.EventName, event.Distance)
    print("")

#dispaly the results of swimmers
swimmers = session.query(Swimmer).all()
for swimmer in swimmers:
    print(f"ID: {swimmer.id}, Name: {swimmer.Name}, Age: {swimmer.Age}, Gender: {swimmer.Gender}, Team ID: {swimmer.Team_id}")

