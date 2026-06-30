from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask
import os
from dotenv import load_dotenv


load_dotenv()
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")


app = Flask(__name__)                    # this gets the name of the file so Flask knows it's name
# proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY
app.debug = True
toolbar = DebugToolbarExtension(app)

@app.route("/")                          # this tells you the URL the method below is related to
def hello_world():
    return "<p>Hello, World!</p>"        # this prints HTML to the webpage
  
if __name__ == '__main__':               # this should always be at the end
    app.run(debug=True, host="0.0.0.0")
