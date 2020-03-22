from flask_mongoengine import MongoEngine
from flask_bcrypt import generate_password_hash, check_password_hash, Bcrypt

# # Create db engine (we will reflect the app in the main script stubbenshopper)

db = MongoEngine()


# # Drivers

class Drivers(db.Document):
    name = db.StringField(required=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)
    # geo fields
    place = db.StringField()
    street = db.StringField()
    street_number = db.StringField()
    postcode = db.StringField()
    coordinates = db.PointField()
    radius = db.IntField()
    # others
    opens = db.DynamicField() # e.g. {0:[[8,12],[13,18]],1:[[9,12],[13,19]]}
    vehicle_options = db.ListField() # e.g. ["car", "bike"]
    wage = db.StringField()
    contact = db.StringField()
    
    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)


# # Resellers

class Resellers(db.Document):
    name = db.StringField(required=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)
    # geo fields
    place = db.StringField()
    street = db.StringField()
    street_number = db.StringField()
    postcode = db.StringField()
    coordinates = db.PointField()
    radius = db.IntField()
    # others
    rating = db.StringField()
    photo = db.BinaryField()
    about = db.StringField()
    category = db.StringField()
    delivery_options = db.ListField()
    
    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)
