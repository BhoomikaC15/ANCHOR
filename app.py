from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productivity.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)

import models

@app.route('/')
def home():
    return "Productivity Tracker is running YOHOO"
if __name__ == '__main__':
    app.run(debug=True)