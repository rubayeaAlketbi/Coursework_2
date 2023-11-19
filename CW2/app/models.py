from app import db 
from werkzeug.security import generate_password_hash, check_password_hash 


''' User class for database model which user has id, name, email, password. The user 
    relation has one to many relationship with order relation. User can order one or many orders.
    The order has only one user.
'''
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    passwordHashed = db.Column(db.String(100), nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)
    
    # Prevent password from being accessed
    @property
    def password(self):
        raise AttributeError('password: write-only field , not readable')
    # Generate password hash
    @password.setter
    def password(self, password):
        self.passwordHashed = generate_password_hash(password)
    # Verify password hash
    def verify_password(self, password):
        return check_password_hash(self.passwordHashed, password)

''' Merchandise class for database model which merchandise has id, name, price, description.
    The merchandise relation has many to many relationship with animal relation. Merchandise can
    have one or many animals. The animal can have one or many merchandises. The merchandise relation
    has one to many relationship with review relation. Merchandise can have one or many reviews.
    The review can have only one merchandise.
'''
class Merchandise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    animals = db.relationship('Animal', secondary='merchandise_animal', back_populates='merchandises')
    reviews = db.relationship('Review', backref='merchandise', lazy=True)

''' Animal class for database model which animal has id, name, image, description. The animal
    relation has many to many relationship with merchandise relation. Animal can have one or many
    merchandises. The merchandise can have one or many animals.
'''
class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=True)  # This could be a path to the image file
    description = db.Column(db.Text, nullable=True)
    merchandises = db.relationship('Merchandise', secondary='merchandise_animal', back_populates='animals')
    
''' MerchandiseAnimal class for database model which merchandise_animal has id, merchandise_id,
    animal_id. The merchandise_animal relation has many to many relationship with merchandise
    relation. Merchandise can have one or many merchandise_animal. The merchandise_animal can have
    one or many merchandises. The merchandise_animal relation has many to many relationship with
    animal relation. Animal can have one or many merchandise_animal. The merchandise_animal can have
    one or many animals.
'''
class MerchandiseAnimal(db.Model):
    __tablename__ = 'merchandise_animal'
    id = db.Column(db.Integer, primary_key=True)
    merchandise_id = db.Column(db.Integer, db.ForeignKey('merchandise.id'), nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    
''' Order class for database model which order has id, location, payment_method, user_id. The order
    relation has one to many relationship with checkout relation. Order can have one or many checkouts.
'''
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=True)
    payment_method = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.relationship('Checkout', backref='order', lazy=True)

''' Checkout class for database model which checkout has id, order_id, merchandise_id, quantity,
    unit_price, subtotal. The checkout relation has one to many relationship with order relation.
    Checkout can have one or many orders. The order can have one or many checkouts. The checkout
    relation has one to many relationship with merchandise relation. Checkout can have one or many
    merchandises. The merchandise can have one or many checkouts.
'''
class Checkout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    merchandise_id = db.Column(db.Integer, db.ForeignKey('merchandise.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

''' Review class for database model which review has id, comment, rating, merchandise_id. The review
    relation has one to many relationship with merchandise relation. Review can have one or many
    merchandises. The merchandise can have one or many reviews.
'''
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    merchandise_id = db.Column(db.Integer, db.ForeignKey('merchandise.id'), nullable=False)
