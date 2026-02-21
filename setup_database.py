from app import app, db
from models import Car, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Add sample cars
    sample_cars = [
        Car(
            brand="Mercedes-Benz",
            model="S-Class",
            year=2023,
            price=115000.00,
            description="The pinnacle of luxury sedans with advanced technology and unparalleled comfort.",
            image_url="https://images.unsplash.com/photo-1553440569-bcc63803a83d?w=800&h=600&fit=crop",
            available=True
        ),
        Car(
            brand="BMW",
            model="7 Series",
            year=2023,
            price=95000.00,
            description="Executive luxury sedan with cutting-edge technology and powerful performance.",
            image_url="https://images.unsplash.com/photo-1555212697-194d092e3b8f?w=800&h=600&fit=crop",
            available=True
        ),
        Car(
            brand="Audi",
            model="A8",
            year=2023,
            price=89000.00,
            description="Sophisticated luxury with quattro all-wheel drive and premium interior.",
            image_url="https://images.unsplash.com/photo-1555353540-64580b51c258?w=800&h=600&fit=crop",
            available=True
        ),
        Car(
            brand="Porsche",
            model="911 Turbo S",
            year=2023,
            price=215000.00,
            description="Iconic sports car with blistering performance and everyday usability.",
            image_url="https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&h=600&fit=crop",
            available=True
        ),
        Car(
            brand="Tesla",
            model="Model S Plaid",
            year=2023,
            price=135000.00,
            description="Electric performance sedan with insane acceleration and long range.",
            image_url="https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=800&h=600&fit=crop",
            available=True
        ),
        Car(
            brand="Range Rover",
            model="Autobiography",
            year=2023,
            price=165000.00,
            description="Ultimate luxury SUV with off-road capability and exquisite craftsmanship.",
            image_url="https://images.unsplash.com/photo-1550340499-a6c60fc8287c?w=800&h=600&fit=crop",
            available=True
        )
    ]
    
    for car in sample_cars:
        db.session.add(car)
    
    # Create test user
    test_user = User(
        username="testuser",
        email="test@example.com",
        password=generate_password_hash("password123"),
        is_admin=False
    )
    db.session.add(test_user)
    
    db.session.commit()
    print("Sample data added successfully!")