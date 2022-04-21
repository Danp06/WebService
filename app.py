from itertools import count
from time import struct_time
from fastapi import FastAPI, HTTPException, Query
# from numpy import append, number
from pydantic import BaseModel
from typing import Optional
from datetime import *

# from pytz import HOUR


class People(BaseModel):
    """ People constructor object.

        :param id: id of person.
        :type id: int
        :param cod: codigo of person.
        :type cod: str
        :param name: name of person.
        :type name: str
        :param rol: rol of person.
        :type rol: int
        :returns: Person object
        :rtype: object
    """
    id: int
    cod: str
    nombre: str
    rol: int


class Vehicle(BaseModel):
    """
    Class use to represent a register of a vehicle
    
    :param id: Identification of register
    :type id: str
    :param person: person informacion 
    :type person: Object(People) 
    :param status:
    :type status: bool
    :param placa:
    :type placa: str
    :param fecha_ingreso:
    :type fecha_ingreso: datetime
    :param anotaciones:
    :type anotaciones: str
    """
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
vehicles = []


@app.get('/', tags=["Home"])
def home():
    return {"Welcome": "Bienvenidos al Sistema de Control de Acceso Vehicular"}


@app.get('/people', tags=["People"])
def list_people():
    """ Retorna objeto personas en str.
          :returns: object person
          :rtype: str
    """
    return Data


@app.post('/people', tags=["People"])
def create_people(person: People):
    """ Funcion para crear y retornar personas en str.
            :returns: Person object.
            :rtype: str.
    """
    Data.append(person.dict())
    return Data[-1]


@app.get('/people/{id}', tags=["People"])
def find_people(id: int):
    """ Funcion para buscar y retornar una persona en str.
            :returns: Person object.
            :rtype: str.
    """
    for person in Data:
        if person["id"] == id:
            return person
    raise HTTPException(status_code=404, detail="Person not found")


@app.delete('/people/{id}', tags=["People"])
def delete_people(id: int):
    """ Funcion para eliminar personas.
            :returns: Person object.
            :rtype: str.
    """
    for index, person in enumerate(Data):
        if person["id"] == id:
            Data.pop(index)
            return {"message": "Person has been delete succesfully"}
    raise HTTPException(status_code=404, detail="Person not found")


@app.put('/people/{id}', tags=["People"])
def update_person(id: int, updatedperson: People):
    """ Funcion para actualizar y retornar personas en str.
            :returns: Person object.
            :rtype: str.
    """
    for index, person in enumerate(Data):
        if person["id"] == id:
            Data[index]["id"] = id
            Data[index]["nombre"] = updatedperson.dict()["nombre"]
            Data[index]["rol"] = updatedperson.dict()["rol"]
            return {"message": "Person has been updated succesfully"}
    raise HTTPException(status_code=404, detail="Person not found")


@app.get('/register', tags=["Vehicle"])
def registers():
    """ Retorna objeto vehicle en str.
          :returns: object vehicle
          :rtype: str
    """
    return vehicles


@app.post('/register', tags=["Vehicle"])
def create_register(vehicle: Vehicle):
    """ Funcion para crear y retornar vehicle en str.
            :returns: vehicle object.
            :rtype: str.
    """
    vehicles.append(vehicle.dict())
    return vehicle


@app.get('/register/{placa}', tags=["Vehicle"])
def get_register(placa: str):
    """ Funcion para buscar y retornar un vehicle en str.
            :returns: vehicle object.
            :rtype: str.
    """
    vehicles_found = []
    for register in vehicles:
        if register['placa'] == placa:
            vehicles_found.append(register)
            return vehicles_found
    raise HTTPException(status_code=404, detail="Vehicle not found")


@app.get('/register/', tags=["Vehicle"])
def get_register_hours(hour_max: datetime, hour_min: datetime):
    """ Funcion para buscar un vehicle a una hora y retornar cantidad de vehiculos.
            :returns: cantidad vehiculos.
            :rtype: int.
    """
    vehicles_found = []
    number_vehicles = 0
    for register in vehicles:
        if register['fecha_ingreso'] >= hour_min and register['fecha_ingreso'] <= hour_max and \
                register['status'] is True:
            vehicles_found.append(register)
            number_vehicles = number_vehicles + 1
            return {'number of vehicles:': number_vehicles}
    raise HTTPException(status_code=422, detail="invalid semantics")


@app.put('/register/{placa}/', tags=["Vehicle"])
def update_register(placa: str, vehicle: Vehicle):
    """ Funcion para actualizar y retornar vehicle en str.
            :returns: vehicle object.
            :rtype: str.
    """
    vehicle_found = []
    for register in vehicles:
        if register['placa'] == placa and register['status'] is True:
            vehicles[register] = vehicle
            vehicle_found.append(vehicle.dict())
            return {'vehiculo': vehicle.placa, 'información actualizada': vehicle_found}
    raise HTTPException(status_code=404, detail="Vehicle not found")


@app.get('/registre/{rol}', tags=["Vehicle"])
def get_vehicles_by_status(rol: int):
    """ Funcion para buscar un vehiculos parqueados y retornar cantidad de vehiculos por rol.
            :returns: cantidad vehiculos por rol.
            :rtype: int.
    """
    number_registers = [0, 0, 0, 0]
    for register in vehicles:
        if register['person']['rol'] == 0 and register['status'] is True:
            x = number_registers[0]
            number_registers.append(x+1)
        if register['person']['rol'] == 1 and register['status'] is True:
            x = number_registers[1]
            number_registers.append(x+1)
        if register['person']['rol'] == 2 and register['status'] is True:
            x = number_registers[2]
            number_registers.append(x+1)
        if register['person']['rol'] == 3 and register['status'] is True:
            x = number_registers[3]
            number_registers.append(x+1)
        return {'rol:': rol, 'vehiculos parqueados:': number_registers[rol]}
