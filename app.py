
from itertools import count
from time import struct_time
from fastapi import FastAPI, HTTPException, Query
from numpy import append, number
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from pytz import HOUR

class People(BaseModel):
    id: str 
    nombre: str = ''
    rol: int = '0'

class Vehicle(BaseModel):
    id: str
    person: People 
    status: bool = False
    placa: str = "000aaa"
    fecha_ingreso:  datetime = datetime.now()
    anotaciones: str = 'ninguna'

app = FastAPI(
    title="Sistema de Control de Acceso Vehicular"
)

Data = []
vehicles= []

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
def find_people(id: str):
    for person in Data:
        if person["id"] == id:
            return person
    raise HTTPException(status_code=404, detail="Person not found")


@app.delete('/people/{id}', tags=["People"])
def delete_people(id: str):
    for index, person in enumerate(Data):
        if person["id"] == id:
            Data.pop(index)
            return {"message": "Person has been delete succesfully"}
    raise HTTPException(status_code=404, detail="Person not found")


@app.put('/people/{id}', tags=["People"])
def update_person(id: str, updatedperson: People):
    for index, person in enumerate(Data):
        if person["id"] == id:
            Data[index]["id"] = id
            Data[index]["nombre"] = updatedperson.dict()["nombre"]
            Data[index]["rol"] = updatedperson.dict()["rol"]
            return {"message": "Person has been updated succesfully"}
    raise HTTPException(status_code=404, detail="Person not found")

@app.get('/register')
def registers():
    return  vehicles

@app.post('/register')
def create_register(vehicle: Vehicle):
    vehicles.append(vehicle.dict())
    return vehicle

@app.get('/register/{placa}')
def get_register(placa: str ):
    vehicles_found = []
    for register in vehicles:
        if register['placa']==placa:
            vehicles_found.append(register)
    return  vehicles_found 


@app.get('/register/')
def get_register_hours(hour_max: datetime, hour_min: datetime):
    vehicles_found = []
    number_vehicles = 0 
    for register in vehicles:
        if register['fecha_ingreso']>=hour_min and register['fecha_ingreso']<=hour_max:
            vehicles_found.append(register)
            number_vehicles = number_vehicles + 1
    return  {'number of vehicles:':number_vehicles} 

@app.put('/register/{placa}/')
def update_register(placa: str, vehicle: Vehicle):
    vehicle_found = []
    for register in vehicles:
        if register['placa']==placa and register['status']==True:
            vehicles[register] = vehicle
            vehicle_found.append(vehicle.dict())  
        print(vehicle_found)
    return {'vehiculo': vehicle.placa, 'información actualizada': vehicle_found}

@app.get('/registre/{rol}')
def get_vehicles_by_status(rol: int, status = True):
    number_registers = 0
    for register in vehicles:
        for register in vehicles:
            if register['person']['rol']==0 and register['status']==True:
                number_registers +=1
            if register['rol']==1 and register['status']==True:
                number_registers +=1
            if register['rol']==2 and register['status']==True:
                number_registers +=1
            if register['rol']==3 and register['status']==True:
                number_registers +=1            
    return {'rol:':rol, 'vehiculos parqueados:':number_registers}