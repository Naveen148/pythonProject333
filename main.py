from typing import Optional

from fastapi import FastAPI, Depends, Response
from . import schemas, db, model
from .db import engine
from sqlalchemy.orm import Session

app = FastAPI()

get_db = db.get_db
model.Base.metadata.create_all(engine)


@app.get("/")
def index():
    return {"Check": "Docs Page"}


@app.get("/addresses/")
def get_all(db: Session = Depends(get_db)):
    address = db.query(model.Address).all()
    return address


@app.post('/createaddress/', response_model=schemas.Address)
def create_address(request: schemas.Address, db: Session = Depends(get_db)):
    new_address = model.Address(**request.dict())
    print(new_address)
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address


@app.get('/addresses/{id}')
def get_address(id: int, db: Session = Depends(get_db)):
    address = db.query(model.Address).filter(model.Address.id == id).first()
    return address


@app.delete('/addresses/{id}')
def delete_address(id: int, db: Session = Depends(get_db)):
    address = db.query(model.Address).filter(model.Address.id == id).first()
    db.delete(address)
    db.commit()
    return {"message": "Address deleted"}


@app.put('/addresses/{id}', response_model=schemas.Address)
def update_address(id: int, request: schemas.Address, db: Session = Depends(get_db)):
    address = db.query(model.Address).filter(model.Address.id == id).first()
    address.street = request.street
    address.city = request.city
    address.state = request.state
    address.zip = request.zip
    address.lat = request.lat
    address.lng = request.lng
    db.commit()
    return address


# retrieve all the addresses that are between the coordinates
@app.get('/addresses/{lat}/{lng}')
def get_address_by_coordinates(lat: float, lng: float, db: Session = Depends(get_db)):
    address = db.query(model.Address).filter(model.Address.lat <= lat, model.Address.lng <= lng).all()
    return address

