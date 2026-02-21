from app import app, db
from models import Car

sample_cars = [
    {
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2023,
        "price": 25000.00,
        "description": "Reliable and fuel-efficient sedan with modern features.",
        "image_url": "https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?w=800&h=600&fit=crop",
        "available": True
    },
    {
        "brand": "Honda",
        "model": "Civic",
        "year": 2023,
        "price": 28000.00,
        "description": "Sporty design with excellent fuel economy.",
        "image_url": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800&h=600&fit=crop",
        "available": True
    },
    {
        "brand": "Mercedes-Benz",
        "model": "S-Class",
        "year": 2023,
        "price": 115000.00,
        "description": "Luxury sedan with cutting-edge technology.",
        "image_url": "https://images.unsplash.com/photo-1553440569-bcc63803a83d?w=800&h=600&fit=crop",
        "available": True
    },
    {
        "brand": "BMW",
        "model": "X5",
        "year": 2023,
        "price": 85000.00,
        "description": "Luxury SUV with powerful performance.",
        "image_url": "https://images.unsplash.com/photo-1555212697-194d092e3b8f?w=800&h=600&fit=crop",
        "available": True
    },
    {
        "brand": "Toyota",
        "model": "Fortuner",
        "year": 2023,
        "price": 45000.00,
        "description": "Robust SUV with excellent off-road capability.",
        "image_url": "https://images.unsplash.com/photo-1563720223485-85756d06134f?w=800&h=600&fit=crop",
        "available": True
    },
    {
        "brand": "Suzuki",
        "model": "Mehran",
        "year": 2022,
        "price": 15000.00,
        "description": "Economical and reliable city car.",
        "image_url": "https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&h=600&fit=crop",
        "available": True
    },
    {
        "brand": "Toyota",
        "model": "Land Cruiser",
        "year": 2023,
        "price": 120000.00,
        "description": "Premium SUV with luxury features.",
        "image_url": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=800&h=600&fit=crop",
        "available": True
    },
    {
        "brand": "Honda",
        "model": "City",
        "year": 2023,
        "price": 30000.00,
        "description": "Comfortable sedan with advanced features.",
        "image_url": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=800&h=600&fit=crop",
        "available": True
    },
    {
        "brand": "Audi",
        "model": "A4",
        "year": 2023,
        "price": 55000.00,
        "description": "Luxury car with quattro all-wheel drive.",
        "image_url": "https://images.unsplash.com/photo-1555353540-64580b51c258?w=800&h=600&fit=crop",
        "available": True
    },
    {
        "brand": "Hyundai",
        "model": "Tucson",
        "year": 2023,
        "price": 35000.00,
        "description": "Modern SUV with smart features.",
        "image_url": "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=800&h=600&fit=crop",
        "available": True
    }
]

with app.app_context():
    for car_data in sample_cars:
        car = Car(
            brand=car_data["brand"],
            model=car_data["model"],
            year=car_data["year"],
            price=car_data["price"],
            description=car_data["description"],
            image_url=car_data["image_url"],
            available=car_data["available"]
        )
        db.session.add(car)
    
    db.session.commit()
    print("✅ 10 sample cars added successfully!")