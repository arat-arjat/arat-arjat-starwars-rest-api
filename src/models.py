from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    #favorite_character = db.relationship('FavoriteCharacter')
    #favorite_planet = db.relationship('FavoritePlanet')

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active":self.is_active 
            # do not serialize the password, its a security breach
        }
    
class Character(db.Model):
    __tablename__ = 'character'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    gender = db.Column(db.String(250))
    eye_color = db.Column(db.String(250), nullable=False)
    #favorite_character = db.relationship('FavoriteCharacter')

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "gender": self.gender,
            "eye_color": self.eye_color,
            # do not serialize the password, its a security breach
        }    

class Planet(db.Model):
    __tablename__ = 'planet'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    poblation = db.Column(db.String(250))
    weather = db.Column(db.String(250), nullable=False)
    #favorite_planet = db.relationship('FavoritePlanet')

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "poblation": self.poblation,
            "weather": self.weather,
            # do not serialize the password, its a security breach
        }   


class FavoriteCharacter(db.Model): 
    __tablename__ = 'favorite_character'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_id_relationship = db.relationship(User)
    character_id = db.Column(db.Integer, db.ForeignKey('character.uid'))
    character_id_relationship = db.relationship(Character)

    def __repr__(self):
        return '<FavoriteCharacter %r>' % self.character_id

    def serialize(self):
        return {
            "uid": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            # do not serialize the password, its a security breach
        }   

class FavoritePlanet(db.Model): 
    __tablename__ = 'favorite_planet'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_id_relationship = db.relationship(User)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.uid'))
    planet_id_relationship = db.relationship(Planet)

    def __repr__(self):
        return '<FavoritePlanet %r>' % self.planet_id

    def serialize(self):
        return {
            "uid": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            # do not serialize the password, its a security breach
        }  

   