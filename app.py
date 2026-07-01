# from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, render_template, url_for, flash, redirect, request
import os
from dotenv import load_dotenv
import git



load_dotenv()
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")


app = Flask(__name__)                    # this gets the name of the file so Flask knows it's name
# proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY
app.debug = True
# toolbar = DebugToolbarExtension(app)

@app.route("/")                          # this tells you the URL the method below is related to
def hello_world():
    return "<p>Hello, World But this time with a webhook again</p>"        # this prints HTML to the webpage

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
