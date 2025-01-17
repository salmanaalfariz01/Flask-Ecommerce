from sqlalchemy import ForeignKey, LargeBinary, create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Database connection string (replace with your actual connection string)
engine = create_engine('mysql+pymysql://admin_store:123456@localhost/store') 
Base = declarative_base()  # No need to import from sqlalchemy.ext.declarative anymore

#For Men
image_path = r"C:\Users\Salma\Downloads\python\Flask-Ecommerce\frontend\images\shirt\men\15\2.jpg"
#For Women
#image_path = r"C:\Users\Salma\Downloads\python\Flask-Ecommerce\frontend\images\shirt\women\15\1.jpg"
#For Kid
#image_path = r"C:\Users\Salma\Downloads\python\Flask-Ecommerce\frontend\images\shirt\kids\15\1.jpg"


# Image table definition
class Image(Base):
    __tablename__ = 'shirt_images'

    id = Column(Integer, primary_key=True)
    shirt_id = Column(Integer, ForeignKey('shirts.id'), nullable=False)
    image_data = Column(LargeBinary, nullable=False)
    image_path = Column(String(255), nullable=False)

# Model for the Shirts table
class Shirt(Base):  # Use Base instead of db.Model
    __tablename__ = 'shirts'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)
    gender = Column(String(50), nullable=False)

    # Relationships
    images = relationship('Image', backref='shirt', cascade="all, delete-orphan")  # Referencing the Image table

    def __repr__(self):
        return f"<Shirt(id={self.id}, name={self.name}, category={self.category}, gender={self.gender})>"

# Create tables (if they don't exist)
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Find the image record that you want to update (replace 31 with your actual shirt_id or image id)
image_to_update = session.query(Image).filter_by(shirt_id=30, id=44).first()

# Check if the image exists and update the fields
if image_to_update:
    # Update the image data
    with open(image_path, 'rb') as f:
        image_to_update.image_data = f.read()
    
    # Optionally, update the image path if you want to change it
    image_to_update.image_path = image_path

    # Commit the changes to the database
    session.commit()

    # Print the updated values
    print(f"Image with shirt_id={image_to_update.shirt_id}, id={image_to_update.id} has been updated.")
    print(f"New image path: {image_to_update.image_path}")
else:
    print("Image with the given shirt_id not found.")

# Close the session
session.close()
