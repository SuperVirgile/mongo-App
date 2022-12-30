from pymongo import MongoClient

#On ouvre notre connection avec notre base de données MongoDB
client = MongoClient('localhost', 27017)
db = client['Cartier']
collection = db['Virgile']

# Création des coordonnées
def creation_coordonnees(collection):
  
    documents = collection.find()
    for doc in documents:
     
        longitude = float(doc['longitude'])
        latitude = float(doc['latitude'])
        

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
