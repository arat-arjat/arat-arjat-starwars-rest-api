"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, FavoriteCharacter, FavoritePlanet 
import json
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    resultado = User.query.all() 
    if resultado== []: 
        return jsonify({"MSG":"No existen usuarios"}), 404
    response_body= list(map( lambda item:item.serialize(),resultado ))
    return jsonify(response_body), 200

@app.route('/character', methods=['GET'])
def get_character():

    resultado = Character.query.all() 
    if resultado== []: 
        return jsonify({"MSG":"No existen personajes"}), 404
    response_body= list(map( lambda item:item.serialize(),resultado ))
    return jsonify(response_body), 200

@app.route('/planet', methods=['GET'])
def get_planet():

    resultado = Planet.query.all() 
    if resultado== []: 
        return jsonify({"MSG":"No existen planet"}), 404
    response_body= list(map( lambda item:item.serialize(),resultado ))
    return jsonify(response_body), 200

@app.route('/planet/<int:planet_uid>', methods=['GET'])
def get_individual_planet(planet_uid):

    resultado = Planet.query.filter_by(uid=planet_uid).first() 
    if resultado is None: 
        return jsonify({"MSG":"No existen planet"}); 404
    return jsonify(resultado.serialize()), 200 

@app.route('/character/<int:character_uid>', methods=['GET'])
def get_individual_character(character_uid):

    resultado = Character.query.filter_by(uid=character_uid).first() 
    if resultado is None: 
        return jsonify({"MSG":"No existen character"}); 404
    return jsonify(resultado.serialize()), 200 

@app.route('/user/<int:user_id>', methods=['GET'])
def get_individual_user(user_id):

    resultado = User.query.filter_by(id=user_id).first() 
    if resultado is None: 
        return jsonify({"MSG":"No existen user"}); 404
    return jsonify(resultado.serialize()), 200 

@app.route('/favorite/planet/<int:planet_uid>', methods=['POST'])
def post_individual_planet(planet_uid):
 
    body= json.loads(request.data)
    new_favortie = FavoritePlanet(
        user_id= body["user_id"],
        planet_id = planet_uid  
    )
    db.session.add(new_favortie)
    db.session.commit()
    return jsonify({"MSG":" Planeta favorito creado "}), 200

@app.route('/favorite/character/<int:character_uid>', methods=['POST'])
def post_individual_character(character_uid):
 
    body= json.loads(request.data)
    new_character = FavoriteCharacter(
        user_id= body["user_id"],
        character_id = character_uid  
    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify({"MSG":" character favorito creado "}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_individual_planet(planet_id):

    user_id = request.args.get("user_id")
    favorite_delete_planet= FavoritePlanet.query.filter_by(user_id = user_id, planet_id = planet_id).first()
    if favorite_delete_planet: 
        db.session.delete(favorite_delete_planet)
        db.session.commit()
        return jsonify({"MSG":" Planeta favorito eliminado "}), 200
    return jsonify({"MSG":" Planeta favorito no eliminado "}), 400

@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_individual_character(character_id):

    user_id = request.args.get("user_id")
    favorite_delete_character= FavoriteCharacter.query.filter_by(user_id = user_id, character_id = character_id).first()
    if favorite_delete_character: 
        db.session.delete(favorite_delete_character)
        db.session.commit()
        return jsonify({"MSG":" Character favorito eliminado "}), 200
    return jsonify({"MSG":" Character favorito no eliminado "}), 400


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
