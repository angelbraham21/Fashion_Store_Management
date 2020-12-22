from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_cors import cross_origin
import pandas as pd
import pyodbc

employee = { "Priyanka" : "priyanka", "Smitha" : "smitha", "Eldho" : "eldho", "Baslin" : "baslin", "Annabel" : "annabel"}


#connection to database
conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=LAPTOP-2MAKJBVK\SQLEXPRESS;'
                      'Database=Store_Management;'
                      'Trusted_Connection=yes;')


app = Flask(__name__)
app.secret_key = 'hello'    #Secret key.

@app.route('/')             #This is a decorator.
@cross_origin()
def home():
    return render_template('index11.html')


@app.route('/login', methods=['POST','GET']) 
@cross_origin()
def login():
    flag = 0
    if request.method == 'POST':
        user = request.form['name']   #'name' is the name of the dictionary key.
        pwd = request.form['password']
        for key, value in employee.items():
            if key == user and value == pwd:
                session['user'] = user      #'user' is the name of the dictionary key.
                #flash("Login Succesful!")
                return redirect(url_for("products"))
                flag = 1
                break
        if flag == 0:
            flash("INCORRECT USERNAME or PASSWORD !!")
            return redirect(url_for('login'))
    else:
        if 'user' in session:       #Check notes 446-448.
            flash("Already logged in")
            return redirect(url_for('products'))

        return render_template('login.html')


@app.route('/user')
@cross_origin()
def user():
    if 'user' in session:
        user = session['user']
        return render_template('user.html', user = user)
    else:
        flash("You are not logged in yet.")
        return redirect(url_for('login'))


@app.route('/logout')
@cross_origin()
def logout():
    #The next 3 lines of code is for checking if the user is in the session. And if he is there then we will logout with the user name.
    if 'user' in session:
        user = session['user']
        flash(f"You have succesfully logged out, {user}.","info")
    session.pop('user',None)    #Remove the user data from our sessions. None is a message associated with removing that data.
    return redirect(url_for('home'))


@app.route("/Customers", methods = ["GET", "POST"])
@cross_origin()
def Customers():
    data1 = pd.read_sql("SELECT * FROM Customers", conn)
    result=data1.to_html()
    return result


    
@app.route("/Employees", methods = ["GET", "POST"])
@cross_origin()
def Employees():
    data2 = pd.read_sql("SELECT * FROM Employees", conn)
    result=data2.to_html()
    return result

@app.route("/products", methods = ["GET", "POST"])
@cross_origin()
def products():
    data3 = pd.read_sql("SELECT * FROM products", conn)
    result=data3.to_html()
    return result


@app.route("/Time", methods = ["GET", "POST"])
@cross_origin()
def Time():
    data4 = pd.read_sql("SELECT * FROM Time", conn)
    result=data4.to_html()
    return result


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug = True) 
#The "debug = True" will make the server update by itself and make the changes for us.
