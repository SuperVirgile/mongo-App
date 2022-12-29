from pymongo import MongoClient

#On ouvre notre connection avec notre base de données MongoDB
client = MongoClient('localhost', 27017)
db = client['Cartier']
collection = db['Virgile']

def creation_coordonnees(collection):
    #Cela nous permet d'itérer sur chaque document
    documents = collection.find()
    for doc in documents:
        #On récupère les longitudes et latitudes dans chacun de nos documents
        longitude = float(doc['longitude'])
        latitude = float(doc['latitude'])
        #Nous faisons ici notre update en faisant passer les valeurs récupérés plus haut - on s'assure de bien updater l'ID de chaque document
        #grâce à la variable doc['_id'] !
        collection.update({"_id":doc['_id']},{"$set": {"loc" :
            {"type":"Point",
            "coordinates" : [
            longitude,
            latitude
            ]
            }}})
        print("done for doc ID : #" + str(doc['_id']))
    print("All done, your documents are updated !")


creation_coordonnees(collection)
