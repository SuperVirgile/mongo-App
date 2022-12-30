# 1 Set-up Mongo DB :
Ouvrir une connection -> sudo mongo dans le terminal
Créer une collection -> mongoimport --db #nomDossier --collection #nomCollection --file
yelp_academic_dataset_business_las_vegas.json
# 2 Pré traitement :
Run pre_traitement.py pour créer un attribut 'loc' comprenant les coordonnées
# 3 Add index :
Run dans le shell db.getCollection('#nomCollection').createIndex(loc : "2dsphere")
# 4 Add index :
Run dans le shell db.getCollection('#nomCollection').createIndex({name : "text", categories :"text"})
# 5 Run :
Run mongoapp.py dans le dossier mongoApp
