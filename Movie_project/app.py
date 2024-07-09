from atexit import register
import importlib
from msilib.schema import IniLocator
from multiprocessing import connection
from sqlite3 import Cursor
from turtle import distance
from urllib import response
from flask import Flask,request ,render_template,request, session,url_for,redirect,flash
import pickle
from numpy import repeat
import requests
import pandas as pd
from patsy import dmatrices
from forms import RegistrationForm, loginForm
import email_validator
from flask_mysqldb import MySQL
from requests.exceptions import ConnectionError, Timeout, RequestException
import time

movies = pickle.load(open('Model/movies_list.pkl','rb'))
similarity = pickle.load(open('Model/similarity.pkl','rb'))

def fetch_poster(movie_id, api_key, retries=2):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            poster_path = data['poster_path']
            full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
            return full_path
        except (ConnectionError, Timeout) as e:
            print(f"Network error: {e}. Retrying...")
            time.sleep(5)  # Wait for 5 seconds before retrying
        except RequestException as e:
            print(f"Request failed: {e}")
            break  # Do not retry on other types of request exceptions
    return None


def recommend(movie):
    index = movies[movies['title']==movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True ,key=lambda x: x[1]) 
    recommend_movies_name = []
    recommend_movies_poster =[]
    for i in distances[1:7]:
        movie_id = movies.iloc[i[0]].movie_id
        api_key = "3d37c2fac22fe027806e896fb80c0c2a"
        recommend_movies_poster.append(fetch_poster(movie_id,api_key))
        recommend_movies_name.append(movies.iloc[i[0]].title)
        
    return recommend_movies_name, recommend_movies_poster
    
app=Flask(__name__)

app.config['SECRET_KEY'] ='7b0e1519dafd49051ee114ab59b3d12b'
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "project"

mysql = MySQL(app)


@app.route("/")
@app.route("/Home")
def Home():
    return render_template('Home.html')


@app.route("/About")
def About():
    return render_template('About.html')


@app.route("/Contact",methods=['GET','POST'])
def Contact():
    if request.method == "POST":
        print(request.form)
        flash(f'Thank you for your submission!','success')
       
        return redirect(url_for('Home')) 
    return render_template('Contact.html')


@app.route("/login",methods=['GET', 'POST'])
def login():
    form = loginForm()
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM register WHERE username=%s AND password=%s',(username,password))
        record=cursor.fetchone()
        cursor.close()
        if record:
            session['loggedin']=True
            session['username']=record[1]
            return redirect(url_for('Home'))
        else:
            msg = 'Incorrect username/password.Try again!'
    return render_template('login.html',form = form)


@app.route("/Register",methods=['GET', 'POST'])
def Register():
    form = RegistrationForm()
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO register(Username,email,password,confirm_password) VALUES (%s,%s,%s,%s)",(username,email,password,confirm_password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('Home'))
    return render_template('Register.html',form = form)

@app.route("/Recommendation" , methods = ['GET', 'POST'])
def Recommendation():
    movie_list = movies['title'].values
    status = False
    if request.method == "POST":
        try:
            if request.form:
                movies_name = request.form['movies']
                print(movies_name)
                recommend_movies_name,recommend_movies_poster = recommend(movies_name)
                status = True
                print(recommend_movies_name)
                print(recommend_movies_poster)
                return render_template('Recommendation.html',movies_name = recommend_movies_name, poster = recommend_movies_poster, movie_list = movie_list,status= status)
            
        except Exception as e :
            error = {'error':e}
            return render_template('Recommendation.html',error = error, movie_list = movie_list,status= status)
        
    else:
        return render_template('Recommendation.html',movie_list = movie_list,status= status)
        
           
    

if __name__ == '__main__':
    app.run(debug=True)

