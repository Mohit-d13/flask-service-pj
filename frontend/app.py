from flask import Flask, render_template, request, flash, url_for, redirect
import requests
from dotenv import load_dotenv
import os
import json

app = Flask(__name__)

load_dotenv()
backend_uri = os.getenv('BACKEND_URI')      # Backend URI for backend link
app.secret_key = os.getenv('SECRET_KEY')    # Secret key for error messages


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        form_data = request.form
        form_dict = form_data.to_dict()
        
        error = None
        if not form_dict['username']:
            error = "Username is required."
        if not form_dict['email']:
            error = "Email is required."
        if not form_dict['password1']:
            error = "Password is required."
        if form_dict['password1'] != form_dict['password2']:
            error = "Passwords do not match."
            
        if error is None:
            # convert from_dict to json format
            json_data = json.dumps(form_dict)
            response = requests.post(f"{backend_uri}/submit", json=json_data)
            if response.status_code == 200:
                return redirect(url_for('submit'))
            else:
                error = "Failed to submit data."
        
        flash(error)
         
    return render_template('signup.html')

@app.route('/submit', methods=['GET'])
def submit():
    return render_template('submit.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)