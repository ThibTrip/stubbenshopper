#!/usr/bin/env python
# coding: utf-8
# %%
import re
import os
import datetime
import pymongo
from flask import Flask, request
from flask_mongoengine import MongoEngine
from flask_restplus import Api, Resource
from mongoengine.errors import NotUniqueError
from mongoengine.errors import ValidationError


# %% [markdown]
# # Configuration

# %%
app = Flask(__name__)
api = Api(app=app, version='1', title='Stubbenshopper Api', description='', validate=True)
app.config['SECRET_KEY'] = '769üvicvdsokGUZ098dsakjdioucwe8998'
app.config['MONGODB_SETTINGS'] = {'host': os.environ['MONGO_URI_WIRVSVIRUS'],
                                  'connect': True}
db = MongoEngine(app=app, config=app.config)


# %% [markdown]
# # MongoDB document models

# %%
class Users(db.Document):
    email = db.EmailField(required=True, unique=True)
    feedback = db.StringField(required=False)
    user_category = db.StringField(required=True)
    zip_code = db.StringField(required=True)


# %% [markdown]
# # Routes

# %% [markdown]
# ## SignupApi

# %%
@api.route('/subscribe')
class Info(Resource):
    def post(self):
        # collect JSON request body
        data = request.get_json()
        if not data:
            data = {"response": "Invalid request body"}
            return data, 405
        else:
            # check data
            # check we have the keys we need
            expected_keys = set(('email', 'user_category', 'zip_code'))
            missing_keys = expected_keys - set(data.keys())
            if missing_keys:
                missing_keys = ', '.join(list(missing_keys))
                return {"response": f"Invalid request body, keys missing: {missing_keys}"}, 406
            # check user category
            allowed_user_categories = ('reseller', 'driver')
            if not data['user_category'] in allowed_user_categories:
                return {"response": f"Invalid request body, user_category must be one of: {allowed_user_categories}"}, 407
            # save data
            data['email'] = data['email'].strip().lower()
            doc = Users(**data)
            try:
                doc.save()
            except NotUniqueError as e:
                return {"response": "Email already subscribed!"}, 408
            except ValidationError as e:
                return {"response": "Invalid Email address"}, 409
            return {'response':'You have successfully subscribed to the newsletter!'}, 200

# %% [markdown]
# # Run

# %%
if __name__ == '__main__':
    app.run()
