from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class People(BaseModel):
    id: int
    cod : str
    nombre: str
    rol: int


app = FastAPI(
    title="Sistema de Control de Acceso Vehicular"
)

Data = []


@app.get('/', tags=["Home"])
def home():
    return {"Welcome": "Bienvenidos al Sistema de Control de Acceso Vehicular"}


@app.get('/people', tags=["People"])
def list_people():
    return Data


@app.post('/people', tags=["People"])
def create_people(person: People):
    Data.append(person.dict())
    return Data[-1]


@app.get('/people/{id}', tags=["People"])
def find_people(id: int):
    for person in Data:
        if person["id"] == id:
            return person
    raise HTTPException(status_code=404, detail="Person not found")


@app.delete('/people/{id}', tags=["People"])
def delete_people(id: int):
    for index, person in enumerate(Data):
        if person["id"] == id:
            Data.pop(index)
            return {"message": "Person has been delete succesfully"}
    raise HTTPException(status_code=404, detail="Person not found")


@app.put('/people/{id}', tags=["People"])
def update_person(id: int, updatedperson: People):
    for index, person in enumerate(Data):
        if person["id"] == id:
            Data[index]["id"] = id
            Data[index]["nombre"] = updatedperson.dict()["nombre"]
            Data[index]["rol"] = updatedperson.dict()["rol"]
            return {"message": "Person has been updated succesfully"}
    raise HTTPException(status_code=404, detail="Person not found")
