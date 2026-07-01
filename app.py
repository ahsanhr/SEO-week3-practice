# from flask_debugtoolbar import DebugToolbarExtension              # this doesnt work 
from flask import Flask, render_template, url_for, flash, redirect, request
import os
from dotenv import load_dotenv
import git
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy

load_dotenv()
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

app = Flask(__name__)                    # this gets the name of the file so Flask knows it's name
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY
app.debug = True
# toolbar = DebugToolbarExtension(app)              #yeah this doesnt work 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"

with app.app_context():
  db.create_all()


@app.route("/")                          # this tells you the URL the method below is related to
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')

# def hello_world():
#     return "<p>Hello, World But this time with a webhook again again</p>"        # this prints HTML to the webpage

@app.route("/second_page")
def second_page():
    return render_template('second_page.html', subtitle='Second Page', text='This is the second page')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)

@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/SEOweek3practice/SEO-week3-practice')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
  
if __name__ == '__main__':               # this should always be at the end
    app.run(debug=True, host="0.0.0.0")
