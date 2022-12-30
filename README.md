# 1 Set-up Mongo DB :
Ouvrir une connection -> sudo mongo dans le terminal
Créer une collection -> mongoimport --db #nomDossier --collection #nomCollection --file
yelp_academic_dataset_business_las_vegas.json
# Run pre_traitement.py pour créer un attribut 'loc' comprenant les coordonnées
# Run dans le shell db.getCollection('#nomCollection').createIndex(loc : "2dsphere")
# Run dans le shell db.getCollection('#nomCollection').createIndex({name : "text", categories :"text"})
# Run mongoapp.py dans le dossier mongoApp
