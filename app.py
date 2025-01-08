from re import M
from flask import jsonify, Flask, make_response, redirect, render_template, request, url_for
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, get_jwt_identity, jwt_required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from webscraper  import scrape_and_store

app = Flask(__name__)
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False  
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'  
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  

app.config['SECRET_KEY'] = 'dev'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
# creates SQLALCHEMY object
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Applications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    opportunity_id = db.Column(db.String(50), nullable=False)

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/dashboard')
@jwt_required()
def dashboard():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user:
        df = scrape_and_store()
        opportunities = df.to_dict(orient='records')
        return render_template('dashboard.html', username=user.username, opportunities=opportunities)
    else:
        return redirect(url_for('signin'))

@app.route('/sign-in', methods=['GET', 'POST'])
def signin():
    if request.method == "GET":
        return render_template('signin.html')
    elif request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            access_token = create_access_token(identity=str(user.id))
            response = make_response(redirect(url_for('dashboard')))  # Redirect to the dashboard
            response.set_cookie('access_token_cookie', access_token, httponly=True)  # Set JWT in a cookie
            return response
        else:
            return render_template('signin.html', error="Invalid credentials")


@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template('signup.html')  # Render the sign-up page
    elif request.method == "POST":
        # Use request.form to get form data
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the user already exists
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('signup.html', error="User already exists.")
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return render_template('signin.html', success="Account created! Please sign in.")

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('signin')))
    response.delete_cookie('jwt')
    return response
    
@app.route('/applications', methods=['GET'])
@jwt_required()
def applications():
    user = User.query.get(get_jwt_identity())
    if user:
        applications = Applications.query.filter_by(user_id=user.id).all()
        return render_template('applications.html', applications=applications)
    else:
        return redirect(url_for('signin'))

@app.route('/profile',methods=['GET','POST'])
@jwt_required()
def profile():
    return render_template('profile.html', user = User)

@app.route('/apply', methods = ['POST'])
@jwt_required()
def apply():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user:
        opportunity_id = request.form.get('opportunity_id')
        new_application = Applications(user_id=user.id, opportunity_id=request.form.get('opportunity_title'))
        db.session.commit()
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('signin'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)