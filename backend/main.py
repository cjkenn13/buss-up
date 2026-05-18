from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx # lets python call busapi
import os #read api key
from dotenv import load_dotenv
import xmltodict

load_dotenv() #reads . end file

API_KEY = os.getenv("THEBUS_API_KEY")#grabss value of api key from .env

app = FastAPI() #creates fastapi. this app objet is wha teverything is attache to
                #every endpoint we make gets added to this object

app.add_middleware(#cross origin resource sharing
    #middleware allows different ports to talk to each other to test locally
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],#front end 5173
    #backend 8000

    #allows origin is the list of frontends allowed to talk to backend, currently just react
    allow_methods=["*"],#allows http(get,post)
    allow_headers=["*"],#allow headers with requests
)

#first endpoint to test
@app.get("/")#decorater, tells fastapi to run this when someone does a get request
def home():#function runs when url is called
    return{"mesasage": "Buss Up API is running!"}#fastpi converste this python dict to JSON

@app.get("/arrivals/{stop_id}")#creates endpoint at arrivals, stop id is variable example, /arriavls/4287
async def get_arrivals(stop_id: str):#async pause and wait for api to respond, stop_id:str means fastapi grabs stopid from url and passes it as string
    url = f"http://api.thebus.org/arrivals/?key={API_KEY}&stop={stop_id}"#builds full bus api url

    async with httpx.AsyncClient() as client:#creates http client(like opening browser), async automaticadlly closes connect when done
        response = await client.get(url)#calls bus api and wait for response.

    data = xmltodict.parse(response.text)#convers raw xml to pythong dictionary
    stop_times = data.get("stopTimes", {})#grabs <stoptimes> section, return {} if empty dictionary
    arrivals = stop_times.get("arrival", [])#same for arriavls

    if isinstance(arrivals, dict):#if single item
        arrivals = [arrivals]#warp in list anyway

    return {
        "stop": stop_times.get("stop"),
        "timestamp": stop_times.get("timestamp"),
        "arrivals": arrivals
    }#gets response from the bus, convert to jason and send bck to endpoint/

# User types stop 4287 in React
# → React calls http://localhost:8000/arrivals/4287
# → FastAPI builds the TheBus URL with your secret API key
# → TheBus sends back arrival data
# → FastAPI sends it to React
# → React displays it on screen