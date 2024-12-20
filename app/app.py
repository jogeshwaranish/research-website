from flask import jsonify, Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/sign-in')
def signin():
    return render_template('signin.html')



@app.route('/sign-up')
def signup():
    return render_template('signup.html')

if __name__ == "__main__":
    app.run(debug=True)