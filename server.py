from flask import Flask, render_template, request, redirect, request, session, flash
from flask_bcrypt import Bcrypt 
from mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]+$')
app = Flask(__name__)
bcrypt = Bcrypt(app)  
app.secret_key="secret key"
mysql = connectToMySQL('loginandregister')


@app.route('/')
def html():
    
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    if len(request.form['email']) < 1:
        flash("Email cannot be blank")
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("That is not an email dude")
    else: 
        mysql=connectToMySQL("loginandregister")
        currentEmails=mysql.query_db("SELECT email FROM users")
        for thing in currentEmails:
            if request.form['email']==thing['email']:
                flash("Email is already taken")
    if len(request.form['first_name']) < 2:
        flash("First name cannot be blank")
    elif not request.form['first_name'].isalpha():
        flash("First name cannot contain numbers")
    if len(request.form['last_name']) < 2:
        flash("Last name cannot be blank")
    elif not request.form['last_name'].isalpha():
        flash("Last name cannot contain numbers")
    if len(request.form['password']) < 8:
        flash("Password must be at least 8 characters")
    if len(request.form['confirm']) < 1:
        flash("Password confirmation cannot be blank")
    if request.form['password'] != request.form['confirm']:
        flash("Password and confirmation must match")
    if '_flashes' in session.keys():
        return redirect("/")
    else:
        pw_hash = request.form['password'] 
        #pw_hash = bcrypt.generate_password_hash(request.form['password']) 
        mysql = connectToMySQL("loginandregister")
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password_hash)s, NOW(), NOW());"
        data = {
             'first_name': request.form['first_name'],
             'last_name': request.form['last_name'],
             'email': request.form['email'],
             'password_hash': pw_hash
           }
        mysql.query_db(query, data)
        return redirect("/success")

@app.route('/login', methods=['POST'])
def login():
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash) 
    if len(request.form['email']) < 1 and len(request.form['password']) < 1:
        flash("Login Data cannot be blank")
        print('email and password too short')
    else:
        mysql=connectToMySQL("loginandregister")
        currentData=mysql.query_db("SELECT * FROM users")
        
        for thing in currentData:
            print(request.form['email'],thing['email'], request.form['password'],thing['password'])
            if request.form['email'] == thing['email'] and request.form['password'] == thing['password']:
                return redirect("/success")
        flash("Email/Password is incorrect !")
        return redirect("/")
    
        

@app.route('/success')
def success():
    return render_template('success.html')






if __name__ == "__main__":
    app.run(debug=True)