from flask import Flask,render_template
from flask import session, g,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy
from check import validations
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = '!9m@S-dThyIlW[pHQbN^'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),nullable =False,unique = True)
    password = db.Column(db.String(20),nullable =False)
    email = db.Column(db.String(50),nullable =False)
    phone_number = db.Column(db.Integer,nullable= False)



@app.route("/signup",methods = ["POST","GET"])
def signup():
    if request.method == "POST" :
        try:
            username = request.form['username']
            records = Todo.query.filter_by(username = username).first() # checking if user already existing.
            if records:
                return " You are already registered, Please login."
            email = request.form['email']
            phone_number = request.form['phone_number']
            password = request.form['password']
            vals = validations(username,password,phone_number,email) # validating user details 
            if vals.validate() == True:
                new_vals = Todo(username = username,password=password,email=email,phone_number=phone_number)
                db.session.add(new_vals) # adding user data to db.
                db.session.commit()
                return " You are registered successfully. Please login"
            else:
                return vals.validate()
        except Exception as e:
            print(e)
            return "Please check input and try again."

@app.route("/login",methods = ["POST","GET"])
def login():
    try:
        if request.method =="POST":
            username = request.form['username']
            password = request.form['password']
            user = Todo.query.filter_by(username = username , password = password).first()
            if user:
                session['logged_in'] = True
                session['username'] = username
                return "Welcome to your profile."
            else:
                return "Invalid username or password."
    except:
        return "Some error occured."

@app.route('/logout/')
def logout():
    try:
        # Removing data from session by setting logged_flag to False.
        session['logged_in'] = False
        # printing logging out message
        return "Successfully logout"
    except:
        return "Some error occured."

@app.route("/profile")
def profile():
    try:
        if session['logged_in'] == True: #checking if there is a user in session.
            return "Welcome to your profile."
        else:
            return "Please login to view your profile."
    except:
        return "Some error occured."

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5) # for creating session for 5 minutes.

if __name__ == "__main__":
    db.create_all() # to create db
    app.run(debug=True)
