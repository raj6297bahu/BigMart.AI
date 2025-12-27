
from flask import Flask, render_template, request, jsonify, url_for, redirect, flash
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

from flask_mail import Mail, Message

app = Flask(__name__, template_folder="templates")
app.secret_key = 'supersecretkey'  # Change this in production!

# Mail Configuration (Using Console for Dev)
# To use real SMTP, replace these with actual credentials
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  
app.config['MAIL_PASSWORD'] = 'your-password'
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'
# Suppress actual sending if config is invalid, but we'll try/except to show log
app.config['MAIL_DEBUG'] = True 

mail = Mail(app)

# Database Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'predictions.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class PredictionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_fat = db.Column(db.Float)
    item_type_val = db.Column(db.Integer)
    outlet_location = db.Column(db.Float)
    outlet_type_val = db.Column(db.Float)
    age = db.Column(db.Float)
    mrp = db.Column(db.Float)
    prediction = db.Column(db.Float)
    item_type_str = db.Column(db.String(50))
    outlet_type_str = db.Column(db.String(50))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Load Model
model2 = pickle.load(open('model.pkl', 'rb'))

# Helper for mapping values back to strings for display
ITEM_TYPE_MAP = {
    0: 'Baking Goods', 1: 'Breads', 2: 'Breakfast', 3: 'Canned', 4: 'Dairy',
    5: 'Frozen Foods', 6: 'Fruits and Vegetables', 7: 'Hard Drinks', 8: 'Seafood',
    9: 'Others', 10: 'Meat', 11: 'Household', 12: 'Health and Hygiene',
    13: 'Snack Foods', 14: 'Soft Drinks', 15: 'Starchy Foods'
}
OUTLET_TYPE_MAP = {
    0: 'Grocery Store', 1: 'Supermarket Type1', 2: 'Supermarket Type2', 3: 'Supermarket Type3'
}

@app.before_request
def create_tables():
    db.create_all()

# Routes
@app.route('/', methods=['GET'])
def landing():
    recent = PredictionHistory.query.order_by(PredictionHistory.id.desc()).limit(5).all()
    display_data = []
    for r in recent:
        display_data.append({
            'item_type': r.item_type_str if r.item_type_str else 'Unknown',
            'outlet_type': r.outlet_type_str if r.outlet_type_str else 'Unknown',
            'item_mrp': "{:.2f}".format(r.mrp),
            'prediction': "{:.2f}".format(r.prediction)
        })
    return render_template('landing.html', recent_predictions=display_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('landing'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', 'error')
        else:
            new_user = User(username=username, email=email, password=generate_password_hash(password, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            
            # Send Welcome Email
            try:
                msg = Message(f"Welcome to Big Mart AI, {username}!",
                              recipients=[email])
                msg.body = f"Hello {username},\n\nYour account has been successfully created. We are excited to have you on board!\n\nBest Regards,\nBig Mart AI Team"
                mail.send(msg)
                flash(f'Account created! Welcome email sent to {email}.', 'success')
            except Exception as e:
                # Log error but don't crash app. 
                print(f"Email failed: {e}")
                flash('Account created successfully! (Email delivery failed due to missing server config)', 'warning')

            return redirect(url_for('landing'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    if request.method == 'POST':
        message = request.form.get('message')
        new_feedback = Feedback(user_id=current_user.id, message=message)
        db.session.add(new_feedback)
        db.session.commit()
        # Simulation of sending email
        print(f"Sending email from {current_user.email}: {message}")
        flash('Feedback submitted successfully!', 'success')
        return redirect(url_for('landing'))
    return render_template('feedback.html')

@app.route('/tool', methods=['GET'])
@login_required
def predict_ui():
    return render_template('prediction.html')

@app.route("/predict", methods=['POST'])
@login_required
def predict():
    if request.method == 'POST':
        Visibility = 0.0539
        try:
            Fat = float(request.form['Item_Fat_Content'])
            Item_type = float(request.form['Item_Type'])
            Location = float(request.form['Outlet_Location_Type'])
            Outlet_type = float(request.form['Outlet_Type'])
            Age = float(request.form['Age_Outlet'])
            Price = float(request.form['Item_MRP'])
            
            prediction_arr = model2.predict([[Fat, Visibility, Item_type, Price, Location, Outlet_type, Age]])
            output = float(prediction_arr[0])
            
            new_entry = PredictionHistory(
                item_fat=Fat,
                item_type_val=Item_type,
                outlet_location=Location,
                outlet_type_val=Outlet_type,
                age=Age,
                mrp=Price,
                prediction=output,
                item_type_str=ITEM_TYPE_MAP.get(int(Item_type), "Unknown"),
                outlet_type_str=OUTLET_TYPE_MAP.get(int(Outlet_type), "Unknown")
            )
            db.session.add(new_entry)
            db.session.commit()
            
            output_str = "{:.2f}".format(output)
            return render_template('prediction.html', prediction_text=output_str)
        except ValueError:
             return render_template('prediction.html', prediction_text="Error: Invalid input")

    return render_template('prediction.html')

@app.route('/api/predict', methods=['POST'])
def predict_api():
    try:
        data = request.json
        Visibility = 0.0539
        
        Fat = float(data.get('Item_Fat_Content'))
        Item_type = float(data.get('Item_Type'))
        Location = float(data.get('Outlet_Location_Type'))
        Outlet_type = float(data.get('Outlet_Type'))
        Age = float(data.get('Age_Outlet'))
        Price = float(data.get('Item_MRP'))
        
        prediction_arr = model2.predict([[Fat, Visibility, Item_type, Price, Location, Outlet_type, Age]])
        output = prediction_arr[0]
        
        return jsonify({'prediction': float("{:.2f}".format(output))})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/dashboard')
@login_required
def dashboard():
    # 1. Sales by Item Type
    item_type_stats = db.session.query(
        PredictionHistory.item_type_str, 
        db.func.count(PredictionHistory.id),
        db.func.avg(PredictionHistory.prediction)
    ).group_by(PredictionHistory.item_type_str).all()
    
    item_type_labels = [s[0] for s in item_type_stats]
    item_type_sales = [float("{:.2f}".format(s[2])) for s in item_type_stats] # Avg Sales

    # 2. Sales by Outlet Type
    outlet_type_stats = db.session.query(
        PredictionHistory.outlet_type_str,
        db.func.avg(PredictionHistory.prediction)
    ).group_by(PredictionHistory.outlet_type_str).all()

    outlet_labels = [s[0] for s in outlet_type_stats]
    outlet_values = [float("{:.2f}".format(s[1])) for s in outlet_type_stats]

    # 3. Visibility vs Sales (Scatter) - Note: Visibility is currently hardcoded in predict, 
    # but we should use 'item_fat' or 'mrp' for better viz if visibility is constant.
    # Let's use MRP vs Prediction for a better scatter plot.
    scatter_data_query = db.session.query(PredictionHistory.mrp, PredictionHistory.prediction).all()
    scatter_data = [{'x': r[0], 'y': r[1]} for r in scatter_data_query]

    return render_template('dashboard.html', 
                           item_type_labels=item_type_labels, 
                           item_type_sales=item_type_sales,
                           outlet_labels=outlet_labels,
                           outlet_values=outlet_values,
                           scatter_data=scatter_data)

if __name__=="__main__":
    app.run(debug=True, port=8000)