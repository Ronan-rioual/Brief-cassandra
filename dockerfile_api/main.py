from fastapi import FastAPI
import uvicorn
from data import DataAccess as da

app = FastAPI(redoc_url=None)

@app.get("/")
async def read_root():
    return {"hello":"world"}


# Amaury    
# accéder aux infos d'un restaurant à partir de son id,
@app.get("/info_resto")
async def info_resto(id_ : int = None):
    da.connexion()
    resultat = da.info_resto(id_=id_)
    da.deconnexion()
    return resultat

# Ronan  
# accéder à la liste des noms de restaurants à partir du type de cuisine,
@app.get("/nom_resto_type_cuisine")
async def nom_resto_type_cuisine(type_cuisine : str = None):
    da.connexion()
    liste = da.nom_resto_type_cuisine(type_cuisine=type_cuisine)
    da.deconnexion()
    return {"Liste de noms" : liste}

# Amaury  
# accéder au nombre d'inspection d'un restaurant à partir de son id restaurant,
@app.get("/nb_inspection_id")
async def nb_inspection_id(id_ : int = None):
    da.connexion()
    resultat = da.nb_inspection_id(id_=id_)
    da.deconnexion()
    return {"nombre d'inspections" : resultat}

# Ronan
# accéder aux noms des 10 premiers restaurants d'un grade donné.
@app.get("/dix_premiers_restos_grade")
async def dix_premiers_restos_grade(grade : str = None):
    da.connexion()
    liste = da.dix_premiers_restos_grade(grade=grade)
    da.deconnexion()
    return {"" : liste}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)