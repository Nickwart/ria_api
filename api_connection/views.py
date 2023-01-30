from bs4 import BeautifulSoup, Tag

from ria_api.authentication import authenticate
from django.http import HttpResponse
from ria_api.settings import RIA_API_KEY, RIA_USER_ID
import requests
import json

from django.views import View
from api_connection.models import (
    Car,
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
    Description, Options, Photo
)


class PublishCar(View):
    def get(self, request):
        # data = request.data
        car = Car.objects.get(id=13)
        url_post_car = f'https://developers.ria.com/auto/used/autos/?user_id={RIA_USER_ID}&api_key={RIA_API_KEY}'
        car_data = {
            "custom": car.custom,
            "year": car.year,
            "price": {
                "value": car.price,
                "currency": {
                    "id": car.currency.ria_id
                }
            },
            "categories": {
                "main": {
                    "id": car.category.ria_id
                }
            },
            "brand": {
                "id": car.brand.ria_id
            },
            "model": {
                "id": car.model.ria_id
            },
            "modification": car.modification,
            "body": {
                "id": car.body.ria_id
            },
            "mileage": car.mileage,
            "region": {
                "id": car.region.ria_id
            },
            "city": {
                "id": car.city.ria_id
            },
            "VIN": car.vin,
            "gearbox": {
                "id": car.gearbox.ria_id
            },
            "drive": {
                "id": car.drive.ria_id
            },
            "fuel": {
                "id": car.fuel.ria_id,
            },
            "engine": {
                "volume": {
                    "liters": car.engine_volume
                }
            },
            "power": {
                "hp": car.engine_power_hp,
                "kW": car.engine_power_kw},
            "color": {
                "id": car.color.ria_id,
            },
            "post": {
                "auctions": False,
                "comments": {
                    "allowed": True,
                    "check": False
                },
            },
            "description": {
                "uk": car.description.ua
            },
            "doors": car.doors,
            "seats": car.seats,
            "spareParts": car.spare_parts
        }
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        response_car_post = requests.post(url_post_car, data=json.dumps(car_data), headers=headers)

        car_adv_id = json.loads(response_car_post.__dict__['_content'])['_id']
        url_add_photos = f'https://developers.ria.com/auto/used/autos/{car_adv_id}/photos/upload?user_id={RIA_USER_ID}&api_key={RIA_API_KEY}'
        photos = Photo.objects.filter(car_id=car.id)
        photo_data = {}
        photo_data.update({'main': photos[0].url})
        photo_links = []
        for photo in photos[1:]:
            photo_links.append(photo.url)
        photo_data.update({'links': photo_links})
        response_photo_post = requests.post(url_add_photos, data=json.dumps(photo_data), headers=headers)

        return HttpResponse(response_car_post, response_photo_post, status=200)


class GetCarData(View):

    def get(self, request):

        def get_photos(url):
            photo_list = []
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'lxml')
            for code_block in soup.body.find_all('div', attrs={'class': 'vertical-tabs__container'}):
                for element in code_block:
                    if isinstance(element, Tag):
                        for thing in element:
                            if isinstance(thing, Tag) and thing.name == 'li':
                                for string in thing:
                                    if string.name == 'img':
                                        photo_list.append(string['data-src'])
            return photo_list

        photos = get_photos(
            "https://autopark.ua/buy/legkovye/vnedorozhnik-krossover/toyota/36567-toyota-landcruiserprado"
)
        data = requests.get(f'http://eligma.com.ua/webhook_handlers/autopark/local_crm_article/{36567}/')
        car_data_json = data.json()
        additional_info = json.loads(car_data_json['type_data'])
        description = Description.objects.create(ua=car_data_json['desc_public'])
        engine_power_kw = car_data_json['kilowatt']
        if car_data_json['kilowatt'] == "":
            engine_power_kw = 0
        new_car = Car.objects.create(
            autopark_id=car_data_json['id'],
            custom=int(car_data_json['rastamogka']),
            year=int(car_data_json['yom_public']),
            price=int(car_data_json['price_public']),
            currency=Currency.objects.get(autopark_id=int(car_data_json['currency_public'])),
            category=Categories.objects.get(autopark_id=int(car_data_json['type'])),
            brand=Brand.objects.get(autopark_id=int(car_data_json['brand'])),
            model=CarModel.objects.get(autopark_id=int(car_data_json['model'])),
            modification=car_data_json['modification'],
            body=Body.objects.get(autopark_id=int(car_data_json['body'])),
            mileage=int(car_data_json['mileage']),
            region=Region.objects.get(autopark_id=int(car_data_json['region'])),
            city=City.objects.get(autopark_id=int(car_data_json['city_id'])),
            vin=car_data_json['cert_vin'],
            gearbox=Gearbox.objects.get(autopark_id=int(car_data_json['transmission'])),
            drive=Drive.objects.get(autopark_id=int(car_data_json['gear'])),
            fuel=Fuel.objects.get(autopark_id=int(car_data_json['fuel'])),
            engine_volume=float(car_data_json['capacity']),
            engine_power_hp=car_data_json['horsepower'],
            engine_power_kw=engine_power_kw,
            color=Color.objects.get(autopark_id=int(car_data_json['color'])),
            doors=int(car_data_json['cabin_doors']),
            seats=int(car_data_json['cabin_seats']),
            description=description
        )

        # for option_name in additional_info:
        #     new_car.options.add(Options.objects.get(name=option_name))

        for photo_url in photos:
            Photo.objects.create(car=new_car, url=f'https://autopark.ua{photo_url}')

        return HttpResponse(status=201)


# update models views
# class UpdateBodies(View):
#     def get(self, request, **kwargs):
#         if authenticate(request):
#             user = authenticate(request)[0]
#         else:
#             raise UserNotLoggedInException


