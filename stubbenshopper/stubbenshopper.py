#!/usr/bin/env python
# coding: utf-8
# %%
import re
import os
import datetime
import pymongo
from flask import Flask, request
from flask_jwt_extended import JWTManager
from flask_restplus import Api, Resource
from flask_bcrypt import Bcrypt
from databases import db, Drivers, Resellers
from routes import create_signup_route, create_login_route


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
db.init_app(app, config=app.config)

# %% [markdown]
# ## POST send_info

# %%
create_signup_route(api=api, route='/reseller/signup', db_cls_model=Resellers)
create_signup_route(api=api, route='/drivers/signup', db_cls_model=Resellers)
create_login_route(api=api, route='/reseller/login', db_cls_model=Drivers)
create_login_route(api=api, route='/drivers/login', db_cls_model=Drivers)

# %%
"update_profile"
"update_business_hours"
"update_contact_info"

# %% [markdown]
# # Run

# %%
if __name__ == '__main__':
    app.run()
