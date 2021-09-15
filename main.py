from flask import Flask
from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import query
from wtforms import *
from wtforms.validators import *
from wtforms.validators import DataRequired
from flask import flash

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
    password = PasswordField("Password", validators=[validators.length(min=6, max=16),validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField("Repeat Password")

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
def register():
    form = UserRegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = Users(username=form.username.data, name=form.name.data,email= form.email.data,password= form.password.data, address=form.address.data, phone_number= form.phone_number.data, activate=False)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('register'))
    return render_template('userregister.html', form=form)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)