from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db,Owner, Pet
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    host = request.path
    return f'<h1> Request Header {host} </h1>'

@app.route('/owner/<int:id>')  #Owner route
def owner_by_id(id):  #endpoint A.K.A function
    owner = Owner.query.filter(Owner.id == id).first() #Fetch First owner found

    if not owner: #Handle error if owner is not found
        response_body = '<h1>Error 404</h1>'
        response = make_response(response_body, 404)
        return response
    
    response_body = f' <h1>{owner.name} </h1>'
    pets = [pet for pet in owner.pets] #get all pets associated to the owner

    if not pets: #If owner Does not have a pet
        response_body += f'<h1> Has no Pet </h1>'
    
    else: 
        for pet in pets: #loop through all pets
            response_body += f'<h2> Has pet {pet.species} named {pet.name} </h2>'
    
    response = make_response(response_body, 200)

    return response

@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()

    if not pet:
        response_body = '<h1> Error 404 </h1>'
        response = make_response(response_body, 404)
        return response
    
    response_body = f'<h2>Has Pet {pet.species} named {pet.name} owned by {pet.owner.name} </h2>'
    response = make_response(response_body, 200)
    return response

@app.route('/<string:classname>')
def classname(classname):
    host = request.path
    return f'<h1> This class is {host}</h1>'

@app.route('/count/<int:param>')
def count_param(param):
    print(param)
    numbers = '\n'.join(str(i) for i in range(param))
    print(numbers)
    return f'<h1>{numbers}</h1>'

if __name__ == '__main__':
    app.run(port=5555)