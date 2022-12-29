from flask import Flask
from flask import request
from flask import render_template
from pymongo import MongoClient
import folium

#Pour pouvoir utiliser FLASK !
app = Flask(__name__)

#On ouvre notre connection avec notre base de données MongoDB
client = MongoClient('localhost', 27017)
db = client['Cartier']
collection = db['Virgile']

app.config['TEMPLATES_AUTO_RELOAD'] = True

def get_docs_by_query_and_gps(query, lat, long, distance) :
    docs = collection.find({
    "$and" : [
    {"$text": { "$search": query }}, #notre requête va aller chercher l'index text que nous avons créé
    {"loc":{ "$geoWithin": { "$centerSphere": [ [lat, long], distance / 6378.1 ] } } } #la latitude et la longitude sont transférées ici
    ] #la division de distance par le diamètre de la planète terre (une sphère)
    },
    {"_id": 0, "name" : 1, "address" : 1, "categories" : 1, "stars" : 1} #les catégories que nous choisissons d'afficher -> reste simple et indicatif !
    )
    return(list(docs[:10])) #nous limitons les résultats de notre requêtes aux 10 premiers éléments trouvés

#On utilise ici folium pour générer notre carte :
def get_map(query, lat, long, distance) :
    coordonnees = collection.find({
    "$and" : [
    {"$text": { "$search": query }},
    {"loc":{ "$geoWithin": { "$centerSphere": [ [lat, long], distance / 6378.1 ] } } }
    ]
    },
    {"_id": 0, "name" : 1, "loc.coordinates":1}
    ).limit(10)
    # On va se référer à l'endroit où se trouve l'utilisateur pour que la carte soit centré dessus
    map = folium.Map(width=750,height=600, location=[long,lat], zoom_start=12)
    folium.Marker(location=[long,lat],icon=folium.Icon(icon="home")).add_to(map) #l'icône de notre utilisateur
    #Ajoute la localisation de tous les résultats de la requête - on change l'icône pour que ça envoie quelque chose de différent ! -> les restau en orange !
    for coord in list(coordonnees):
        folium.Marker(location = sorted(coord["loc"]["coordinates"], reverse=True), popup = coord["name"], icon = folium.Icon(color="orange")).add_to(map)
    return(map)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/', methods=['POST'])
def text_box():
    text = request.form['text'] #nous récupérons les inputs utilisateurs
    longitude = float(request.form['longitude'])
    latitude = float(request.form['latitude'])
    distance = float(request.form['distance'])
    map = get_map(text, longitude, latitude, distance).save('templates/map.html') #transférés à notre fonction get_map, on génère un html qu'on intègre dans notre html
    docs = get_docs_by_query_and_gps(text, longitude, latitude, distance) #transférés à notre fonction get_docs
    return render_template("result.html", docs = docs)

if __name__ == '__main__':
    app.run()
