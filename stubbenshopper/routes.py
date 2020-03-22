from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_restplus import Resource


def create_signup_route(api, route, db_cls_model):
    """
    Registers a route to sign up to our app.
    
    Parameters
    ----------
    api : flask_restplus.Api
    route : str
    db_cls_model : cls
        A class inheriting a MongoEngine.Document and containing at least:
        * An attribute "password"
        * The method "hash_password" to hash the the attribute password
    """
    @api.route(route)
    class SignupApi(Resource):
        def post(self):
            data = request.get_json()
            instance =  db_cls_model(**data)
            instance.hash_password()
            instance.save()
            return {'id': str(instance.id)}, 200

def create_login_route(api, route, db_cls_model):
    """
    Registers a route to log in to our app.
    
    Parameters
    ----------
    api : flask_restplus.Api
    route : str
    db_cls_model : cls
        A class inheriting a MongoEngine.Document and containing at least:
        * An attribute "email" (primary key, used to log in)
        * An attribute "password" (a hashed password)
        * The method "check_password" to check the hashed password
    """
    @api.route(route)
    class LoginApi(Resource):
        def post(self):
            body = request.get_json()
            instance = db_cls_model.objects.get(email=body.get('email'))
            authorized = db_cls_model.check_password(body.get('password'))
            if not authorized:
                return {'error': 'Email or password invalid'}, 401
            expires = datetime.timedelta(days=7)
            access_token = create_access_token(identity=str(instance.id), expires_delta=expires)
            return {'token': access_token}, 200


def create_update_route(api, route, db_cls_model, expected_fields):
    """
    Registers a route to update a mongo document.
    
    Parameters
    ----------
    api : flask_restplus.Api
    route : str
    db_cls_model : cls
        A class inheriting a MongoEngine.Document with various fields
    expected_fields : list
        Which fields to expect (on the absence of any field an error 
        response is returned)
    """
    @api.route(route)
    class UpdateRoute(Resource):
        @jwt_required
        def post(self):
            # collect JSON request body
            data = request.get_json()
            if not data:
                data = {"response": "Invalid request body"}
                return data, 404
            else:
                expected_fields_present = (set(expected_fields) - set(data.keys())) == set()
                if not expected_fields_present:
                    fields_str = ', '.join(expected_fields)
                    return {'response':f'Expected all the following fields to be present: {fields_str}'}, 403
                instance = db_cls_model(**data)
                likes.save({'favorite_fruit':favorite_fruit,
                            'favorite_color':favorite_color})
                return {'response':'success!'}, 200
