from website import Flask, create_app 
from werkzeug.serving import run_simple


app = create_app()

if __name__ == "__main__":
    run_simple('0.0.0.0',80, app)
    #app.run(host='0.0.0.0', port= 80)