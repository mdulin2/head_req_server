'''
Make sure Flask is installed for Python3. 
Run: 
    - python3 main.py
Requests: 
    - Use tester.py with one of the below routes
    - Or, use curl at http://127.0.0.1:5000
'''

from flask import Flask
from flask import request

app = Flask(__name__)

## Allows for both HEAD and GET requests. 
@app.route("/")
def home():
    print("GET")
    return "Hello, World!"
    
@app.route("/salvador")
def salvador():
    return "Hello, Salvador"

## Safe way 
'''
The exact checks make this possible. With a HEAD request, the server just errors. 
This is because nothing is returned. 
'''
@app.route("/login-safe", methods=["GET", "POST"])
def log_in_safe():

    if(request.method == "POST"):
        print("POST LOGIN")
        return "POST LOGIN"
        # Attempt the login & do something else
    elif(request.method == "GET"):
        print("GET LOGIN")
        return "GET LOGIN" 

''' 
Allows for a head request because the GET is included. 
If the GET is removed, then the HEAD is not allowed. 
This is vulnerable to an implicit method assumption issue. 
'''
@app.route("/login-unsafe", methods=["GET", "POST"])
def log_in_unsafe():

    if(request.method == "GET"):
        print("GET LOGIN")
        return "GET LOGIN"
        # Attempt the login & do something else
    else:
        print("POST LOGIN")
        return "POST LOGIN" 

if __name__ == "__main__":
    app.run(debug=True)