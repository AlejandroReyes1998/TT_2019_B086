from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = "Secret Key"
#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:''@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#Creating model table for our CRUD database
class Data(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	apaterno = db.Column(db.String(100))
	amaterno = db.Column(db.String(100))
	username = db.Column(db.String(100))
	password = db.Column(db.String(100))
	email = db.Column(db.String(100))
	phone = db.Column(db.String(100))
	speciality = db.Column(db.String(100))
	city = db.Column(db.String(100))
	def __init__(self, name, apaterno,amaterno,username,password,email, phone,speciality,city):
		self.name = name
		self.apaterno = apaterno
		self.amaterno = amaterno
		self.username = username
		self.password = password
		self.email = email
		self.phone = phone
		self.speciality = speciality
		self.city = city
#This is the index route where we are going to
#query on all our employee data
@app.route('/')
def Index():
	all_data = Data.query.all()
	return render_template("index.html", employees = all_data)
#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():
	if request.method == 'POST':
		password = request.form['password']
		confpassword =request.form['password1']
		if password == confpassword:
			name = request.form['name']
			apaterno = request.form['apaterno']
			amaterno = request.form['amaterno']
			email = request.form['email']
			phone = request.form['phone']
			username = request.form['username']
			speciality = request.form['speciality']
			city = request.form['city']
			my_data = Data(name, apaterno,amaterno,username,password,email,phone,speciality,city)
			db.session.add(my_data)
			db.session.commit()
			flash("¡Registro creado!")
			return redirect(url_for('Index'))
		else:
			flash("¡Las contraseñas no coinciden!")
			return redirect(url_for('Index'))
#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():
	if request.method == 'POST':
		my_data = Data.query.get(request.form.get('id'))
		password = request.form['password']
		confpassword = request.form['password1']
		if password == confpassword:
			my_data.password = request.form['password']
			my_data.name = request.form['name']
			my_data.apaterno = request.form['apaterno']
			my_data.amaterno = request.form['amaterno']
			my_data.email = request.form['email']
			my_data.phone = request.form['phone']
			my_data.username = request.form['username']
			my_data.speciality = request.form['speciality']
			my_data.city = request.form['city']
			db.session.commit()
			flash("¡Registro actualizado!")
			return redirect(url_for('Index'))
		else:
			flash("¡Las contraseñas no coinciden!")
			return redirect(url_for('Index'))
#This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
	my_data = Data.query.get(id)
	db.session.delete(my_data)
	db.session.commit()
	flash("¡Registro eliminado!")
 
	return redirect(url_for('Index'))

if __name__ == "__main__":
	app.run(debug=True)