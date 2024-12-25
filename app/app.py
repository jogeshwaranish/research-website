from flask import jsonify, Flask, make_response, render_template, request
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid

app = Flask(__name__)

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

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/sign-in', methods=['GET', 'POST'])
def signin():
    if request.method == "GET":
        return render_template('signin.html')  # Render the sign-in page
    elif request.method == "POST":
        # Use request.form to get form data
        username = request.form.get('username')
        password = request.form.get('password')

        # Authenticate the user
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            access_token = create_access_token(identity=user.id)
            return render_template('dashboard.html', username=username)
        else:
            return render_template('signin.html', error="Invalid username or password.")

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


if __name__ == "__main__":
    app.run(debug=True)