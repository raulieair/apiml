import db
from sqlalchemy import Column, Integer, String, Boolean, Float

class entry(db.Base):
    __tablename__= "entries"

    id = Column(Integer, primary_key=True)
    sepal_length= Column(Float, nullable=False)
    sepal_width=Column(Float, nullable=False)
    petal_length=Column(Float, nullable=False)
    petal_width=Column(Float, nullable=False)
    specie=Column(String(30), nullable=False)

    def __init__(self, sepal_length, sepal_width, petal_length, petal_width, specie):
        self.sepal_length = sepal_length
        self.sepal_width = sepal_width
        self.petal_length = petal_length
        self.petal_width = petal_width
        self.specie = specie

    def __repr__(self):
        return "Entry:{} -> specie:{}".format(self.id, self.specie)
    
    def __str__(self):
        return "Entry:{} -> specie:{}".format(self.id, self.specie)
    
class User(db.Base):
    __tablename__= "users"
    id = Column(Integer, primary_key=True)
    username=Column(String(30), nullable=False)
    password=Column(String(30), nullable=False)

    def __init__(self,  username, password):
        
        self.username = username
        self.password = password
        

    def __repr__(self):
        return "User:{} -> name:{}".format(self.id, self.username)
    
    def __str__(self):
        return "User:{} -> name:{}".format(self.id, self.username)