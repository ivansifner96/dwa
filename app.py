from flask import Flask, Response, jsonify, request, flash, render_template, current_app, redirect
from baza import Korisnik, Zapisnik
import sqlite3
import datetime as dt
import secrets
import os
import functools
import operator


db = sqlite3.connect("baza.sqlite", check_same_thread=False)

app = Flask(__name__)

cur = db.cursor()

@app.route('/')
def pocetak():
	return render_template('pocetnas.html')



@app.route('/lista_filmova', methods=['GET', 'POST'])
def pregled():
	if request.method == 'POST':
		naziv_filma = request.form.get('naziv')
		godina = request.form.get('godina')
		datum_pregleda = dt.datetime.now()
		db.execute("INSERT INTO Zapisnik(naziv_filma, godina, datum_pregleda, korisnik_mail) VALUES (:naziv_filma, :godina, :datum_pregleda, :korisnik_mail)", {"naziv_filma":naziv_filma, "godina":godina, "datum_pregleda":datum_pregleda, "korisnik_mail":korisnik_mail})
		db.commit()
		return render_template('popissvihfilmova.html')
	return render_template('popissvihfilmova.html')

@app.route('/registracija', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')
		email = request.form.get('email')
		potvrda = request.form.get('con_pass')
		if password == potvrda:
			db.execute("INSERT INTO Korisnik(email, username, password) VALUES (:email, :username, :password)", {"email":email, "username":username, "password":password})
			db.commit()
			return render_template('registracija.html')
	return render_template('registracija.html')
	

@app.route('/home', methods=['GET', 'POST'])
def prijava():
	global korisnik_mail;
	if request.method == 'POST':
		password = request.form.get('password')
		email = request.form.get('email')
		e_mail = db.execute("SELECT email FROM Korisnik WHERE email=:email",{"email":email}).fetchone()
		sifra = db.execute("SELECT password FROM Korisnik WHERE password=:password",{"password":password}).fetchone()
		if e_mail is None or sifra is None:
			return render_template('login.html')
		pravi_email = ''.join(e_mail)
		pravi_password = ''.join(sifra)
		if pravi_email == email and pravi_password == password:
			korisnik_mail = email
			return render_template('prvas.html')
		else: 
			return render_template('popissvihfilmova.html')
	return render_template('login.html')

	
@app.route('/moji_filmovi', methods=['GET', 'POST', 'PUT'])
def listaj():
	podaci = db.execute("SELECT naziv_filma, godina, datum_pregleda, id FROM Zapisnik Where korisnik_mail=:korisnik_mail", {"korisnik_mail":korisnik_mail}).fetchall()
	if request.method == 'POST':
		godina = request.form.get('godina')
		button = request.form.get('button1')
		if button is not None:
			print("test")
			print("test2", button)
			db.execute("DELETE FROM Zapisnik WHERE id="+button+"")
			db.commit()
			return render_template('lista_filmova.html', value = podaci)
		elif godina != "":
			godina = int(godina)
			#new_podaci = db.execute("SELECT naziv_filma, godina, datum_pregleda FROM Zapisnik Where godina between :godina and :godina + 10", {"godina":godina}).fetchone()
			#print(new_podaci)
			tuble_problem = db.execute("SELECT naziv_filma, godina, datum_pregleda, id FROM Zapisnik Where godina between :godina and :godina + 10", {"godina":godina}).fetchone()
			print(tuble_problem)
			if tuble_problem is None:
				return render_template('lista_filmova.html', value = podaci)
			elif tuble_problem is not None:
				extra_novi = db.execute("SELECT naziv_filma, godina, datum_pregleda, id FROM Zapisnik Where godina between :godina and :godina + 10 and korisnik_mail=:korisnik_mail", {"godina":godina, "korisnik_mail":korisnik_mail}).fetchall()
				print("yeaah")
				return render_template('lista_filmova.html', value = extra_novi)
		#elif request.method == 'GET':
		#else :
			#print("Tu si")
			#button = request.form.get('button1')
			#print("button je", button)
			#if button != "":
				#print("Uspio si")
				#db.execute("DELETE FROM Zapisnik WHERE id="+button+"")
				#db.commit()
				#return render_template('lista_filmova.html', value=podaci)
	return render_template('lista_filmova.html', value=podaci)
		#db.commit()
		#new_podaci = db.execute("SELECT naziv_filma, godina, datum_pregleda FROM Zapisnik Where korisnik_mail=:korisnik_mail", {"korisnik_mail":korisnik_mail}).fetchall()
		

if __name__ == "__main__":
	app.secret_key=os.urandom(12)
	app.run(debug=True)
