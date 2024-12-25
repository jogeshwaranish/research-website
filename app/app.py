from flask import jsonify, Flask, make_response, render_template, request
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dev'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
# creates SQLALCHEMY object
db = SQLAlchemy(app)

jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(50))


@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/sign-in', methods=['GET', 'POST'])
def signin():
    if (request.method == "GET"):
        return render_template('signin.html')
    elif (request.method == "POST"):
        data = request.get_json()
        user_name = data['Username']
        passwrd = data["Password"]

        user = User.query.filter_by(username = user_name).first()
        if user:
            access_token = create_access_token(identity=user.id)
            return jsonify({"access_token": access_token}), 200
        else:
            return make_response("The account with this username dosen't exist or the password is wrong", 201)

@app.route("/dashboard")

@app.route('/sign-up',methods=['GET', 'POST'])
def signup():
    if (request.method == "GET"):
        return render_template('signup.html')
    elif (request.method == "POST"):
        data = request.get_json()
        user_name = data['Username']
        passwrd = data["Password"]

        users = User.query.filter_by(username = user_name).first()

        if not users:
            users = User(
                id = str(uuid.uuid4()),
                username = user_name,
                password = passwrd )
            db.session.add(users)
            db.session.commit()
        else:
            return make_response("user already exists", 202)

if __name__ == "__main__":
    app.run(debug=True)