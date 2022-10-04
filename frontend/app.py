from flask import Flask ,render_template , url_for
from flask_wtf import FlaskForm
from flask.globals import request
from flask_restful import Api ,Resource
from werkzeug.utils import redirect
import json
import folium
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import   DataRequired,Length, NumberRange
app = Flask(__name__)
api=Api(app)
basePath='/api/v1'
hashtag_list:list=[]
numero_tweet=[1]
app.config['SECRET_KEY'] = 'Thisisasecret!'


class build_data():
    def chek_data():
        form=hashtag_form()
        if len(hashtag_list)>0 and form.iterazioni.data>0:
            print('ho almeno un hash e numero di itetazioni >0',)
        return {
                "data":{
                "hashtag_list":hashtag_list,
                "numero_di_tweet":numero_tweet[ len(numero_tweet)-1]
                }
            }     

def add_hashtag():
    tag = request.form.get('hashtag', '', type=str)
    num=request.form.get('iterazioni', '', type=int)
    hashtag_list.append(tag)
    numero_tweet.append(num)

def cancella_elemento(element):
    hashtag_list.remove(element)


class hashtag_form(FlaskForm) :
    hashtag=StringField(
        u'inserisci Hashtag senza #',
        validators=[
			DataRequired('inserisci un hashtag'),
			Length(1, 16),
		])
    iterazioni = IntegerField(u'numero di tweet', 
    default=1,validators = [DataRequired(), NumberRange(min=1, max=99, message="inserisci un numero da 1 a 99")]
    )
    submit_tag=SubmitField('+')
class get_data(Resource):
    def get(self):
            if not build_data.chek_data():
                return None ,404
            return build_data.chek_data(), 200

api.add_resource(get_data,f'{basePath}/data')

@app.route("/", methods=['GET','POST'])
def index():
    form=hashtag_form()
    if form.is_submitted():
        add_hashtag()
        return redirect(url_for('index'))
    return render_template('index.html',form=form,lista=hashtag_list,numero_tweet=numero_tweet,n=numero_tweet[len(numero_tweet)-1])

@app.route('/cancella-lista/<element>', methods=['GET','POST'])
def cancella_lista(element):
    cancella_elemento(element)
    return redirect(url_for('index'))





@app.route('/invia-dati',methods=['GET','POST'])
def invia_dati():
    return redirect('http://localhost:2000/')


        
@app.route('/map',methods=['GET'])
def map():
    lat=40.96948670403734
    long=14.20805364054345
    start_coords = (lat,long)
    folium_map = folium.Map(location=start_coords, zoom_start=14)
    folium.Marker([lat,long],icon=folium.Icon(icon='cloud')).add_to(folium_map)
    return render_template('invia.html', map=folium_map._repr_html_())

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,  debug=True)


