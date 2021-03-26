import cassandra
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
import uvicorn

class DataAccess :

    @classmethod
    def connexion(cls):
        cls.ap = PlainTextAuthProvider(username="cassandra",password="password123")
        cls.cluster = Cluster(['cassandra_1'], port=9042, auth_provider=cls.ap)
        cls.session = cls.cluster.connect(keyspace="resto")
        cls.session.row_factory = cassandra.query.tuple_factory


    @classmethod 
    def deconnexion(cls):
        cls.cluster.shutdown() # ferme aussi la session

    # accéder aux infos d'un restaurant à partir de son id,
    @classmethod
    def info_resto(cls, id_):
        if type(id_) == int:
            resultat = cls.session.execute("SELECT * FROM restaurant WHERE id = {};".format(id_))
            return list(resultat)
        
    # Ronan  
    # accéder à la liste des noms de restaurants à partir du type de cuisine,
    @classmethod
    def nom_resto_type_cuisine(cls, type_cuisine):
        resultat = cls.session.execute("SELECT name FROM restaurant WHERE cuisinetype = '{}';".format(type_cuisine))
        resultat = [truc[0] for truc in resultat]
        return list(resultat)

    # Amaury  
    # accéder au nombre d'inspection d'un restaurant à partir de son id restaurant,
    @classmethod
    def nb_inspection_id(cls, id_):
        if type(id_) == int:
            resultat = cls.session.execute("SELECT COUNT(*) FROM inspection WHERE idrestaurant = {};".format(id_))
            return list(resultat[0])
    # Ronan
    # accéder aux noms des 10 premiers restaurants d'un grade donné.
    @classmethod
    def dix_premiers_restos_grade(cls, grade):
        resultat = []
        requete = cls.session.execute("SELECT idrestaurant FROM inspection WHERE grade = '{}' LIMIT 10;".format(grade))
        # Sur cassandra, le workflow est différent du relationnel, il faut bâtir ses tables très précisément en fonction
        # des queries qu'on va être amenés à nécessiter. Ici, impossible de faire un simple SELECT DINSTINCT car la restriction
        # de la clause WHERE n'est pas sur une partition key (càd l'autre part que la clustering key dans une composite primary key)
        # et qu'elle n'est pas non plus sur une colonne statique. On externalise donc le "distinct" dans le python (plus simple) :
        requete = list(set(requete)) # retrait des id doublons
        for id_resto in requete:
            id_resto = int(id_resto[0]) # id_resto était un tuple contenant un nombre, on le repasse en simple int
            data = cls.session.execute("SELECT name FROM restaurant WHERE id = {};".format(id_resto))
            resultat.append(data.one()[0]) # on prend le contenu de chaque tuple du cluster ResultSet renvoyé par la requête juste avant.
        return list(resultat)


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)