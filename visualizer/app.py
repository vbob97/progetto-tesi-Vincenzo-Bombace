from flask import Flask,render_template,request
import requests
import json,os,datetime
import folium
import pandas as pd
from geopy.geocoders import Nominatim
app = Flask(__name__)
base='http://cleaner:8000/api/v1/data'

def getFromAPI():
    try: 
        req=requests.get(base).text
        data=json.loads(req)
        df=pd.read_json(data)
    except requests.ConnectionError:
        return "Connection Error"
    
    return df



@app.route('/map',methods=['GET'])
def map():
    df=getFromAPI()
    geolocator = Nominatim(user_agent="my_user_agent")
    #start_coords =(42.96555012189528, 12.32951453624705)
    folium_map = folium.Map(zoom_start=14)
    for pos in df.index:
        if (df['position'][pos] is not None) or (df['position'][pos] is not ''):
                print(df['position'][pos],"dopo l'if")
                g=geolocator.geocode(df['position'][pos])
                if hasattr(g, 'longitude') and hasattr(g, 'latitude'):
                    print(g.latitude,g.longitude,"long")
                    if df['sentiment'][pos]==1:
                        color='blue'
                    else:
                        color='red'

                    folium.Marker([g.latitude,g.longitude],icon=folium.Icon(color=color,icon='twitter',prefix='fa')).add_to(folium_map)
    folium_map
    #folium.Marker([lat,long],icon=folium.Icon(icon='cloud')).add_to(folium_map)
    return render_template('map.html', map=folium_map._repr_html_())


@app.route('/',methods=['GET'])
def filter_data():
    if request.method=='GET':
        df=getFromAPI()
        return render_template('index.html',tables=[df.to_html(classes='data', header="true")])
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9000,  debug=True)