from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Car, Order
from forms import RegistrationForm, LoginForm, CarForm, OrderForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables and add sample data
with app.app_context():
    # Drop and create fresh tables (remove db.drop_all() in production)
    db.drop_all()
    db.create_all()
    
    # Create admin user
    admin = User.query.filter_by(email='admin@carshowroom.com').first()
    if not admin:
        hashed_password = generate_password_hash('admin123')
        admin = User(username='admin', email='admin@carshowroom.com', password=hashed_password, is_admin=True)
        db.session.add(admin)
    
    # Add sample cars (10 cars)
    sample_cars = [
        Car(
            brand='Toyota',
            model='Corolla',
            year=2023,
            price=25000.00,
            description='Reliable and fuel-efficient sedan with modern features. Perfect for family use.',
            image_url='https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?w=800&h=600&fit=crop&auto=format',
            available=True
        ),
        Car(
            brand='Honda',
            model='Civic',
            year=2023,
            price=28000.00,
            description='Sporty design with excellent fuel economy and advanced safety features.',
            image_url='https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800&h=600&fit=crop&auto=format',
            available=True
        ),
        Car(
            brand='Mercedes-Benz',
            model='S-Class',
            year=2023,
            price=115000.00,
            description='Luxury sedan with cutting-edge technology, premium materials, and superior comfort.',
            image_url='https://images.unsplash.com/photo-1553440569-bcc63803a83d?w=800&h=600&fit=crop&auto=format',
            available=True
        ),
        Car(
            brand='BMW',
            model='X5',
            year=2023,
            price=85000.00,
            description='Luxury SUV with powerful performance, spacious interior, and advanced technology.',
            image_url='https://images.unsplash.com/photo-1555212697-194d092e3b8f?w=800&h=600&fit=crop&auto=format',
            available=True
        ),
        Car(
            brand='Toyota',
            model='Fortuner',
            year=2023,
            price=45000.00,
            description='Robust SUV with powerful engine, spacious 7-seater, and excellent off-road capability.',
            image_url='https://images.unsplash.com/photo-1563720223485-85756d06134f?w=800&h=600&fit=crop&auto=format',
            available=True
        ),
        Car(
            brand='Suzuki',
            model='Mehran',
            year=2022,
            price=15000.00,
            description='Economical and reliable city car with low maintenance costs.',
            image_url='https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&h=600&fit=crop&auto=format',
            available=True
        ),
        Car(
            brand='Toyota',
            model='Land Cruiser',
            year=2023,
            price=120000.00,
            description='Premium luxury SUV with all-terrain capability and premium features.',
            image_url='https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=800&h=600&fit=crop&auto=format',
            available=True
        ),
        Car(
            brand='Honda',
            model='City',
            year=2023,
            price=30000.00,
            description='Comfortable sedan with advanced features and spacious interior.',
            image_url='https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=800&h=600&fit=crop&auto=format',
            available=True
        ),
        Car(
            brand='Audi',
            model='A4',
            year=2023,
            price=55000.00,
            description='Luxury car with quattro all-wheel drive and premium interior.',
            image_url='https://images.unsplash.com/photo-1555353540-64580b51c258?w=800&h=600&fit=crop&auto=format',
            available=True
        ),
        Car(
            brand='Hyundai',
            model='Tucson',
            year=2023,
            price=35000.00,
            description='Modern SUV with smart features and stylish design.',
            image_url='https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=800&h=600&fit=crop&auto=format',
            available=True
        )
    ]
    
    # Add all sample cars to database
    for car in sample_cars:
        db.session.add(car)
    
    # Create a test customer user
    test_user = User.query.filter_by(email='customer@test.com').first()
    if not test_user:
        hashed_password = generate_password_hash('test123')
        test_user = User(username='customer', email='customer@test.com', password=hashed_password, is_admin=False)
        db.session.add(test_user)
    
    db.session.commit()
    print("✅ Database created with admin, test user, and 10 sample cars!")

@app.route('/')
def index():
    featured_cars = Car.query.filter_by(available=True).limit(6).all()
    return render_template('index.html', featured_cars=featured_cars)

@app.route('/cars')
def cars():
    brand = request.args.get('brand', '')
    if brand:
        cars = Car.query.filter(Car.brand.ilike(f'%{brand}%'), Car.available==True).all()
    else:
        cars = Car.query.filter_by(available=True).all()
    
    brands = db.session.query(Car.brand).distinct().all()
    brands = [brand[0] for brand in brands]
    
    return render_template('cars.html', cars=cars, brands=brands, selected_brand=brand)

@app.route("/car/<int:car_id>")
def car_detail(car_id):
    car = Car.query.get_or_404(car_id)
    
    # Get all available cars for similar cars section
    all_cars = Car.query.filter_by(available=True).all()
    
    return render_template("car_detail.html", car=car, all_cars=all_cars)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/order/<int:car_id>', methods=['GET', 'POST'])
@login_required
def order_car(car_id):
    car = Car.query.get_or_404(car_id)
    form = OrderForm()
    
    if form.validate_on_submit():
        order = Order(
            user_id=current_user.id,
            car_id=car.id,
            customer_name=form.customer_name.data,
            customer_email=form.customer_email.data,
            customer_phone=form.customer_phone.data,
            customer_address=form.customer_address.data
        )
        db.session.add(order)
        db.session.commit()
        flash('Your order has been placed successfully!', 'success')
        return redirect(url_for('index'))
    
    # Pre-fill form with user data
    if current_user.is_authenticated:
        form.customer_name.data = current_user.username
        form.customer_email.data = current_user.email
    
    return render_template('order.html', car=car, form=form)

# Admin routes
@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))
    
    total_cars = Car.query.count()
    total_orders = Order.query.count()
    total_users = User.query.count()
    recent_orders = Order.query.order_by(Order.order_date.desc()).limit(5).all()
    
    return render_template('admin_dashboard.html', 
                          total_cars=total_cars, 
                          total_orders=total_orders, 
                          total_users=total_users,
                          recent_orders=recent_orders)

@app.route('/admin/cars')
@login_required
def admin_cars():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))
    
    cars = Car.query.all()
    return render_template('admin_cars.html', cars=cars)

@app.route('/admin/cars/add', methods=['GET', 'POST'])
@login_required
def admin_add_car():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))
    
    form = CarForm()
    if form.validate_on_submit():
        car = Car(
            brand=form.brand.data,
            model=form.model.data,
            year=form.year.data,
            price=form.price.data,
            description=form.description.data,
            image_url=form.image_url.data,
            available=form.available.data
        )
        db.session.add(car)
        db.session.commit()
        flash('Car added successfully!', 'success')
        return redirect(url_for('admin_cars'))
    
    return render_template('admin_add_car.html', form=form)

@app.route('/admin/cars/<int:car_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_car(car_id):
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))
    
    car = Car.query.get_or_404(car_id)
    form = CarForm(obj=car)
    
    if form.validate_on_submit():
        car.brand = form.brand.data
        car.model = form.model.data
        car.year = form.year.data
        car.price = form.price.data
        car.description = form.description.data
        car.image_url = form.image_url.data
        car.available = form.available.data
        db.session.commit()
        flash('Car updated successfully!', 'success')
        return redirect(url_for('admin_cars'))
    
    return render_template('admin_edit_car.html', form=form, car=car)

@app.route('/admin/cars/<int:car_id>/delete', methods=['POST'])
@login_required
def admin_delete_car(car_id):
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))
    
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    flash('Car deleted successfully!', 'success')
    return redirect(url_for('admin_cars'))

@app.route('/admin/orders')
@login_required
def admin_orders():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))
    
    orders = Order.query.order_by(Order.order_date.desc()).all()
    return render_template('admin_orders.html', orders=orders)

@app.route('/admin/orders/<int:order_id>/update_status', methods=['POST'])
@login_required
def admin_update_order_status(order_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    if new_status in ['Pending', 'Confirmed', 'Delivered', 'Cancelled']:
        order.status = new_status
        db.session.commit()
        return jsonify({'success': True, 'new_status': new_status})
    
    return jsonify({'error': 'Invalid status'}), 400

if __name__ == '__main__':
    app.run(debug=True)