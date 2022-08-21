from flask import Flask
from waitress import serve
#from views import app
app = Flask(__name__)

if __name__ == "__main copy__":
   #app.run() ##Replaced with below code to run it using waitress 
   serve(app, host='0.0.0.0', port=8000)
