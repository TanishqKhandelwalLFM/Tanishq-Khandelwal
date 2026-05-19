from dotenv import load_dotenv
import os
import requests
import json
import aiohttp
import asyncio
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


load_dotenv()
api_key = os.getenv('WEATHER_API')




cities = ['Delhi','Mumbai','Chennai','Kolkata' , 'Jaipur']
output = []  



class Weather(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    city = db.Column(db.String(50),unique=True,nullable=False)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    description = db.Column(db.String(100))
    temperature = db.Column(db.Float)
    visibility = db.Column(db.Float)
    wind_speed = db.Column(db.Float)

    def __repr__(self):
        return "done"
    
with app.app_context():
    db.create_all()
    

@app.route('/')
def index():
    return "hello this is a weather application"



@app.route('/add')
def add():
    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},india&APPID={api_key}"
        response = requests.get(url)
        data = response.json()

        weather = Weather(
            city=city,
            longitude=data["coord"]["lon"],

            latitude=data["coord"]["lat"],

            description=data["weather"][0]["description"],

            temperature=data["main"]["temp"],

            visibility=data["visibility"],

            wind_speed=data["wind"]["speed"]
        )

        db.session.add(weather)
    db.session.commit()

    return "added"
        

@app.route('/read')
def read():
    data = Weather.query.all()
    output = []

    for d in data :
        output.append({
            "city" : d.city,
            "longitude" : d.longitude,
            "latitude" : d.latitude,
            "description" : d.description,
            "temperature" : d.temperature,
            "visibility" : d.visibility,
            "wind_spped" : d.wind_speed
        })


    return output
















if __name__ == "__main__":
    app.run(debug=True)



def fetch_using_requests() :
    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},india&APPID={api_key}"
        response = requests.get(url)

        output.append({
            city : response.json()
        })

    try :
        with open("weather_data_1.json","w") as file : 
            json.dump(output,file,indent=4)
    except Exception as e :
        print(e)

async def fetch_using_session() :
    output = []
    async with aiohttp.ClientSession() as session :
        for city in cities :
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city},india&APPID={api_key}"

            async with session.get(
                url
            ) as response:

                data = await response.json()

            output.append({
                city : data
            })

    with open("weather_data_2.json","w") as file :
        json.dump(output,file,indent=4)





# async def main () :
#     await fetch_using_session()

# asyncio.run(main())


# fetch_using_requests()
