from flask import Flask

# Creating a Flask Instance
app =  Flask(__name__)

# Defining the starting point, the root.
@app.route('/')

def hello_world():
    return 'Hello World'

@app.route('/extra')

def extra():
    return 'Extra Page'

@app.route('/ages')

def ages():
    year = int(input("What year were you born? "))
    age = (2022 - year)
    print(age)
    return age