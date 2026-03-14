from sqlalchemy.orm import Session
from app.models.building import Building
from app.models.activity import Activity
from app.models.organization import Organization
from app.models.phone import Phone


def seed_data(db: Session):
    if db.query(Building).first():
        return

    b1 = Building(address="г. Москва, ул. Ленина, 1", latitude=55.7558, longitude=37.6173)
    b2 = Building(address="г. Москва, ул. Блюхера, 32/1", latitude=55.7510, longitude=37.6100)

    food = Activity(name="Еда")
    meat = Activity(name="Мясная продукция", parent=food)
    milk = Activity(name="Молочная продукция", parent=food)

    cars = Activity(name="Автомобили")
    trucks = Activity(name="Грузовые", parent=cars)
    parts = Activity(name="Запчасти", parent=trucks)  # это уже 3 уровень

    org1 = Organization(name='ООО "Рога и Копыта"', building=b1)
    org1.phones = [Phone(number="2-222-222"), Phone(number="8-923-666-13-13")]
    org1.activities = [meat, milk]

    org2 = Organization(name='ООО "АвтоМир"', building=b2)
    org2.phones = [Phone(number="3-333-333")]
    org2.activities = [parts]

    db.add_all([b1, b2, food, meat, milk, cars, trucks, parts, org1, org2])
    db.commit()