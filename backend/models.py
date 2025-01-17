from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Updated to match the table
    nama = db.Column(db.String(255), nullable=False)      # Added nama column
    no_hp = db.Column(db.String(15), nullable=False)      # Added no_hp column
    alamat = db.Column(db.Text, nullable=False)           # Added alamat column
    role = db.Column(db.String(15), nullable=True)      # Added role column
    created_at = db.Column(db.DateTime, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'

# Model for the Shirts table
class Shirts(db.Model):
    __tablename__ = 'shirts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)

    # Relationships
    images = db.relationship('ShirtImagesDetail', backref='shirt', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Shirt {self.name}>'

    
    
# Model for the ShirtImagesDetail table
class ShirtImagesDetail(db.Model):
    __tablename__ = 'shirt_images_detail'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shirt_id = db.Column(db.Integer, db.ForeignKey('shirts.id'), nullable=True)
    image_path = db.Column(db.String(255), nullable=True)
    image_data = db.Column(db.LargeBinary, nullable=False)
    color = db.Column(db.String(255), nullable=True)
    size_s = db.Column(db.Integer, nullable=True)
    size_m = db.Column(db.Integer, nullable=True)
    size_l = db.Column(db.Integer, nullable=True)
    size_xl = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return (
            f"<ShirtImagesDetail("
            f"id={self.id}, "
            f"shirt_id={self.shirt_id}, "
            f"image_path='{self.image_path}', "
            f"image_data={'[binary data]' if self.image_data else None}, "
            f"color='{self.color}', "
            f"size_s={self.size_s}, "
            f"size_m={self.size_m}, "
            f"size_l={self.size_l}, "
            f"size_xl={self.size_xl}, "
            f"price={self.price})>"
        )
