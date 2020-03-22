#!/usr/bin/env python
# coding: utf-8
# %%
import re
import os
import datetime
import pymongo
from flask import Flask, request
from flask_bcrypt import generate_password_hash, check_password_hash, Bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager
from flask_mongoengine import MongoEngine
from flask_restplus import Api, Resource


# %% [markdown]
# # Configuration

# %%
app = Flask(__name__)
api = Api(app=app, version='1', title='Stubbenshopper Api', description='', validate=True)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
app.config['SECRET_KEY'] = '769üvicvdsokGUZ098dsakjdioucwe8998'
app.config['MONGODB_SETTINGS'] = {'host': os.environ['MONGO_URI_WIRVSVIRUS'],
                                  'connect': True}
db = MongoEngine(app=app, config=app.config)


# %% [markdown]
# # MongoDB document models

# %%
class Users(db.Document):
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
class Likes(db.Document):
    favorite_fruit = db.StringField(required=True)
    favorite_color = db.StringField(required=True)


# %% [markdown]
# # Routes

# %% [markdown]
# ## SignupApi

# %%
@api.route('/signup')
class SignupApi(Resource):
    def post(self):
        data = request.get_json()
        user =  Users(**data)
        user.hash_password()
        user.save()
        return {'id': str(user.id)}, 200

# %% [markdown]
# ## LoginApi

# %%
@api.route('/login')
class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        user = User.objects.get(email=body.get('email'))
        authorized = user.check_password(body.get('password'))
        if not authorized:
            return {'error': 'Email or password invalid'}, 401
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return {'token': access_token}, 200


# %% [markdown]
# ## POST send_info

# %%
@api.route('/send_info')
class Info(Resource):
    @jwt_required
    def post(self):
        # collect JSON request body
        data = request.get_json()
        if not data:
            data = {"response": "Invalid request body"}
            return data, 404
        else:
            favorite_fruit = data.get('favorite_fruit')
            favorite_color = data.get('favorite_color')
            # check favorite_color and favorite_fruit were provided
            if any((v is None for v in (favorite_fruit, favorite_color))):
                data = {"response": "favorite_fruit or favorite_color missing"}
                return data, 404

            likes = Likes(**data)
            likes.save({'favorite_fruit':favorite_fruit,
                        'favorite_color':favorite_color})
            return {'response':'success!'}, 200


# %%
"update_profile"
"update_business_hours"
"update_contact_info"

# %% [markdown]
# # Run

# %%
if __name__ == '__main__':
    app.run()
