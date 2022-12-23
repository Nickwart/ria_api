from django.test import TestCase
from api_connection.models import (
    Categories,
    Body,
    Brand,
    CarModel,
    Currency,
    Region,
    City,
    Gearbox,
    Drive,
    Fuel,
    Color,
    Country,
    Car
)


class LobbyUserTestCase(TestCase):
    def setUp(self):
        self.category = Categories.objects.create(name='легкові авто', ria_id=1)
        self.body = Body.objects.create(name='седан', ria_id=1)
        self.brand = Brand.objects.create(name='mazda', ria_id=1)
        self.car_model = CarModel.objects.create(brand=self.brand, name='mazda 3', ria_id=1)
        self.currency = Currency.objects.create(name='USD', ria_id=1)
        self.region = Region.objects.create(name='київська область', ria_id=1)
        self.city = City.objects.create(name='київ', ria_id=1)
        self.gearbox = Gearbox.objects.create(name='механіка', ria_id=1)
        self.drive = Drive.objects.create(name='кардан', ria_id=1)
        self.fuel = Fuel.objects.create(name='бензин', ria_id=1)
        self.color = Color.objects.create(name='чорний', ria_id=1)
        self.country = Country.objects.create(name='японія', ria_id=1)
        self.car = Car.objects.create(
            autopark_id=25,
            damage=True,
            custom=True,
            year=2016,
            price=13000,
            currency=self.currency,
            category=self.category,
            brand=self.brand,
            model=self.car_model,
            body=self.body,
            mileage=350000,
            region=self.region,
            city=self.city,
            vin='JKBVNCB164A662141',
            gearbox=self.gearbox,
            drive=self.drive,
            fuel=self.fuel,
            consumption_city=10,
            consumption_route=8,
            consumption_combine=9,
            engine_volume=1.5,
            engine_power_hp=105,
            engine_power_kw=79.0442,
            color=self.color,
            metallic_color=True,
            auctions=True,
            comments_allowed= True,
            comments_check=False,
            video='lLEiT9PeHSg',
            doors=5,
            seats=5,
            country=self.country,
            spareParts=False,
        )

    def test_model_instances_creates(self):
        self.assertEqual(Categories.objects.get(id=1), self.category)
        self.assertEqual(Body.objects.get(id=1), self.body)
        self.assertEqual(Brand.objects.get(id=1), self.brand)
        self.assertEqual(CarModel.objects.get(id=1), self.car_model)
        self.assertEqual(Currency.objects.get(id=1), self.currency)
        self.assertEqual(Region.objects.get(id=1), self.region)
        self.assertEqual(City.objects.get(id=1), self.city)
        self.assertEqual(Gearbox.objects.get(id=1), self.gearbox)
        self.assertEqual(Drive.objects.get(id=1), self.drive)
        self.assertEqual(Fuel.objects.get(id=1), self.fuel)
        self.assertEqual(Color.objects.get(id=1), self.color)
        self.assertEqual(Country.objects.get(name='японія'), self.country)
        self.assertEqual(Car.objects.get(autopark_id=25), self.car)
