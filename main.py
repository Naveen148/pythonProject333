from typing import Optional

from fastapi import FastAPI, Depends, Response
from . import schemas, db, models
from .db import engine
from sqlalchemy.orm import Session

app = FastAPI()

get_db = db.get_db
models.Base.metadata.create_all(engine)


@app.get("/")
def index():
    return {"Check": "Docs Page"}


@app.get("/addresses/")
def get_all(db: Session = Depends(get_db)):
    address = db.query(models.Address).all()
    return address


@app.post('/createaddress/', response_model=schemas.Address)
def create_address(request: schemas.Address, db: Session = Depends(get_db)):
    new_address = models.Address(**request.dict())
    print(new_address)
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address


@app.get('/addresses/{id}')
def get_address(id: int, db: Session = Depends(get_db)):
    address = db.query(models.Address).filter(models.Address.id == id).first()
    return address


@app.delete('/addresses/{id}')
def delete_address(id: int, db: Session = Depends(get_db)):
    address = db.query(models.Address).filter(models.Address.id == id).first()
    db.delete(address)
    db.commit()
    return {"message": "Address deleted"}


@app.put('/addresses/{id}', response_model=schemas.Address)
def update_address(id: int, request: schemas.Address, db: Session = Depends(get_db)):
    address = db.query(models.Address).filter(models.Address.id == id).first()
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
    address = db.query(models.Address).filter(models.Address.lat <= lat, models.Address.lng <= lng).all()
    return address

# @app.get('/addresses/{lat}/{lng}/{radius}')
# def get_address_by_coordinates(lat: float, lng: float, radius: float,db : Session = Depends(get_db)):
#     address = db.query(models.Address).filter(models.Address.lat <= lat, models.Address.lng <= lng, models.Address.lat >= lat - radius, models.Address.lng >= lng - radius).all()
#     geo_location_data = db.engine.execute('select * from ( SELECT  *,( 3959 * acos( cos( radians(6.414478) ) * cos( radians(lat) ) * cos( radians(lng]+' ) - radians(12.466646) ) + sin( radians(6.414478) ) * sin( radians(lat) ) ) ) AS distance FROM Address ) al where distance < dis ORDER BY distance;')
#	  db.session.commit()
#     return address
