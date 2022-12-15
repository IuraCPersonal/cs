# Imports here.
import os
import json
import base64
import pyqrcode
import onetimepass

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, flash, session, abort, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user

from io import BytesIO
from werkzeug.security import generate_password_hash, check_password_hash

from app.utils.caesar.CaesarCipher import CaesarCipher


# Setup Flask and config it.

app = Flask(__name__)

app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True


# Setup other dependecies.

db = SQLAlchemy(app=app)
lm = LoginManager(app=app)
bs = Bootstrap(app=app)


# Setup the User Model.

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))
    otp_secret = db.Column(db.String(16))  # One-time password

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')

    @property
    def password(self):
        raise AttributeError('Unknown Password Attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password=password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password=password)

    def get_totp_uri(self):
        # 👇 https://github.com/google/google-authenticator/wiki/Key-Uri-Format
        return f'otpauth://totp/2FADemo:{self.username}?secret={self.otp_secret}&issuer=2FADemo'

    def verify_totp(self, token):
        return onetimepass.valid_totp(token=token, secret=self.otp_secret)


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    second_password = PasswordField('Enter the password again', validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    token = StringField('Token', validators=[DataRequired(), Length(6, 6)])

    submit = SubmitField('Login')


class CipherForm(FlaskForm):
    input = StringField('Text', validators=[DataRequired(), Length(1, 64)])
    key = StringField('Key', validators=[DataRequired(), Length(1, 64)])

    submit = SubmitField('Encrypt')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result')
def result():
    message = request.args['message']
    
    return render_template('result.html', message=json.loads(message))


@app.route('/classicalciphers', methods=['POST', 'GET'])
def classicalciphers():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = CipherForm()

    if form.validate_on_submit():
        encrypted = CaesarCipher.encrypt(form.input.data, int(form.key.data))
        message = json.dumps({'encrypted': encrypted})

        return redirect(url_for('result', message=message))
    return render_template('classical-ciphers.html', form=form)
        

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is not None:
            flash('Username Already Exists.')
            return redirect(url_for('register'))
        
        user = User(username=form.username.data, password=form.password.data)

        db.session.add(user)
        db.session.commit()

        session['username'] = user.username

        return redirect(url_for('two_factor_setup'))

    return render_template('register.html', form=form)


@app.route('/2FA')
def two_factor_setup():
    if 'username' not in session:
        return redirect(url_for('index'))

    user = User.query.filter_by(username=session['username']).first()

    if user is None:
        return redirect(url_for('index'))

    return render_template('two-factor-setup.html'), 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    }


@app.route('/qrcode')
def qrcode():
    if 'username' not in session:
        abort(404)
    
    user = User.query.filter_by(username=session['username']).first()

    if user is None:
        abort(400)
    
    del session['username']

    # render qrcode for FreeTOTP
    url = pyqrcode.create(user.get_totp_uri())
    stream = BytesIO()
    url.svg(stream, scale=3)

    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    }


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or user.verify_password(form.password.data) == False or \
            not user.verify_totp(form.token.data):
            flash('Wrong username, password or token. Check again!')
            return redirect(url_for('login'))
        
        login_user(user=user)
        flash(f'Welcome, {user.username}.')

        return redirect(url_for('index'))
    
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    
    return redirect(url_for('index'))


if not os.path.exists('db.sqlite'):
    #  call function inside an application context
    with app.app_context():
        db.create_all()


app.run(
    host='0.0.0.0',
    port=5000,
    debug=True
)