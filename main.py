from operator import methodcaller
from flask import Flask
from flask import *
import flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import query
from wtforms import *
from wtforms.validators import *
from wtforms.validators import DataRequired
from flask import flash
from functools import wraps

app=Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/OFY/Desktop/Flask-Library/tmp/test.db'
app.secret_key = 'super secret key'
db = SQLAlchemy(app)


class UserRegisterForm(Form):
    username = StringField('Username', validators=[DataRequired(), validators.length(min=4, max=20)])
    name=StringField("Name Surname", validators=[DataRequired(), validators.length(min=5, max=20)])
    email = StringField("e-Mail", validators=[DataRequired(), validators.Email()])
    address=StringField("Address", validators=[DataRequired()])
    phone_number=StringField("Phone Number", validators=[DataRequired(), validators.length(10)])
    password = PasswordField("Password", validators=[validators.length(min=5, max=16),validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField("Repeat Password")

#USERS DB
class  Users(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=False)
    phone_number = db.Column(db.String(), nullable=False)
    activate = db.Column(db.Boolean(), nullable=False)

@app.route('/')
def IndexPage():
    return render_template('index.html')


#USER REGISTER
@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = Users(username=form.username.data, name=form.name.data,email= form.email.data,password= form.password.data, address=form.address.data, phone_number= form.phone_number.data, activate=False)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('Register'))
    return render_template('register.html', form=form)

#User Login
@app.route('/login', methods=['GET','POST'])
def Login():
    form = UserRegisterForm(request.form)
    l_username = form.username.data
    l_password = form.password.data
    
    if request.method == 'POST':
        try:
            user=Users.query.filter_by(username = l_username).first()
            if user.password == l_password:
                flash("Logged In","success")

                session["logged_in"]=True
                session["username"]=user.username
                #print(user.activate)
                return redirect(url_for("IndexPage"))
            else:
                flash("Wrong Password", "danger")
                return redirect(url_for('Login'))
        except:
            flash("username doesn't exist", "danger")
            return redirect(url_for('Login'))
           
    return render_template('login.html', form=form)

#LOGIN DECORATOR
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "loggec_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Please login","danger")
            return redirect(url_for("Login"))
    return decorated_function

#LOGOUT
@app.route('/logout')
def Logout():
    session.clear()
    return redirect(url_for("IndexPage"))    


#USER UPDATE
@app.route('/update', methods=['GET', 'POST'])
def UserUpdate():
    form = UserRegisterForm(request.form)
    username = session['username']
    user = Users.query.filter_by(username = username).first()
    
    if request.method=='GET':
        form.name.data = user.name
        form.address.data = user.address
        form.email.data  = user.email
        form.phone_number.data = user.phone_number
        form.password.data = user.password
    else: 
        user.name = form.name.data
        user.address = form.address.data
        user.phone_number = form.phone_number.data
        user.email=form.email.data
        user.password=form.password.data
        db.session.commit()
        return redirect(url_for("UserList"))
    

    return render_template('userupdate.html', form=form, user = user)



#USER LIST PAGE
@app.route('/userlist')

def UserList():
    all_users = Users.query.all()
    return render_template('userlist.html', all_users=all_users)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)