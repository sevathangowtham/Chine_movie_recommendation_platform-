# Probem Statement : Chine movie recommondataion system, wants personalized movie recommendations, powered by real TMDB data, with user accounts that remember preferences and favorites.
# THe step to followed 
#1) Import the library which we needed 
#2) Create the class to contain the ID, Name ,Email, so we need tow class one is for Customer detail's onother one is for Favirate movie with Rating , Year of release.
#3) weneed a engine to connect the code and database. 
#4) since we need the user info so we need to create the Post methods with the help of this we can get the user info like name and email so on. 
#5) we can also create one more method for the update so that could help the user to update whenever thay wanted.
#6) all the info is importent so weneed ti store the data in the database.
#7) API key we need so which conataine all the info 

#1) step 1 
import requests
from flask import Flask , request
from sqlalchemy import create_engine ,String, Integer, Float, ForeignKey,Column
from sqlalchemy.orm import declarative_base , sessionmaker

#step 2 

engine = create_engine('sqlite:///chinedatabase.db',echo= False)
Session =sessionmaker(bind=engine)
Base = declarative_base()
session = Session()

#step 3 
class User(Base):
    __tablename__ = 'users'
    ID = Column(Integer, primary_key=True)
    Name = Column(String, nullable=False)
    Email = Column(String, nullable= False, unique=True)

class Fevorate(Base):
    __tablename__ = 'favorates'
    ID = Column(Integer, primary_key=True)
    User_ID = Column(Integer , ForeignKey('users.ID'), nullable= False)
    movie_id = Column(Integer , nullable= False)
    title = Column(String)

Base.metadata.create_all(engine)

app = Flask(__name__)

@app.route('/add_user', methods=['POST'])
def add_user_api():
    data = request. json
    user = User(Name=data['name'], Email=data['email'])
    try : 
        session.add(user)
        session.commit()
    except Exception:  
        session.rollback()
        return {'Message' : 'The user is not added, is mail id already exist!'}
    return {'Message': 'The user added successfully!', 'User_id': user.ID}


#Recommantdataion (Calls TMDB movie API)
@app.route('/recommant',methods = ['POST'])
def faver_recommant():
    data = request.json
    genre_id = data['genre_id']
    min_rating = data['min_rating']
    min_year = data['year']

    url = (f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}'
           f'&with_genres={genre_id}&vote_average.gte={min_rating}'
           f'&primary_release_date.gte={min_year}-01-01')
    responce = requests.get(url)
    movies = responce.json().get('results', [])
    if not movies:
        return {'Message' : 'No movie founds that matching you criteria.'}
    movie_list = []
    for movie in movies:
        movie_list.append({

            'id' : movie['id'],
            'title' : movie['title'],
            'release_date' : movie['release_date'],
            'vote_average' :movie['vote_average']
        })
    return {'Movie' : movie_list}
if __name__ == '__main__':
    app.run(debug=True)