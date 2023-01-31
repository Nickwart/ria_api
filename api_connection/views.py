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
        """
        в цю функцію має зайти тільки айді машини з автопарку, тоді робитьсся запит в БД,
        звідти береться обєкт машини з усіма даними та публікується
        """
        response_car_pub = self.pub_car(36567)
        return HttpResponse(response_car_pub[0], response_car_pub[1], status=200)

    def pub_car(self, autopark_car_id):
        car = Car.objects.get(autopark_id=autopark_car_id)
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
        return [response_car_post, response_photo_post]


class GetCarData(View):

    def get(self, car_id):
        """
        в ідеалі функція приймамє в себе айдішнік машини,
        по ньому робить запит в CRM по основні дані,
        потім робить запит в CRM щоб витягнути юрл оголошення на автопарк,
        закидає його в функцію для витягування фото,
        а потім все гамузом зберігає.
        """
        # ТУТ БИ ВСТАВИТИ ЗАПИТ НА АПІ, ЯКЕ ЗА АЙДІ ВЕРТАТИМЕ УРЛУ ОГОЛОШЕННЯ НА АВТОПАРК
        car_data = self.get_car_data(36567)
        # СЮДИ СОЖНА БУДЕ ВСТАВИТИ ВІДПОВІДЬ РЕКВЕСТУ, тоді в функцію зайде тільки айдішнік
        photos = self.get_photos(
            "https://autopark.ua/buy/legkovye/vnedorozhnik-krossover/toyota/36567-toyota-landcruiserprado"
        )
        self.save_car(car_data, photos)

        return HttpResponse(status=201)

    def get_photos(self, url):
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

    def get_car_data(self, autopark_id):
        data = requests.get(f'http://eligma.com.ua/webhook_handlers/autopark/local_crm_article/{autopark_id}/')
        car_data_json = data.json()
        return car_data_json

    def save_car(self, car_data, photos):

        """
        Ця функція приймає дікт з інформацією про машину,
        список з обрізаними урлами до фото
        і збирає з них запис в базу даних
        """

        additional_info = json.loads(car_data['type_data'])
        description = Description.objects.create(ua=car_data['desc_public'])
        engine_power_kw = car_data['kilowatt']
        if car_data['kilowatt'] == "":
            engine_power_kw = 0
        new_car = Car.objects.create(
            autopark_id=car_data['id'],
            custom=int(car_data['rastamogka']),
            year=int(car_data['yom_public']),
            price=int(car_data['price_public']),
            currency=Currency.objects.get(autopark_id=int(car_data['currency_public'])),
            category=Categories.objects.get(autopark_id=int(car_data['type'])),
            brand=Brand.objects.get(autopark_id=int(car_data['brand'])),
            model=CarModel.objects.get(autopark_id=int(car_data['model'])),
            modification=car_data['modification'],
            body=Body.objects.get(autopark_id=int(car_data['body'])),
            mileage=int(car_data['mileage']),
            region=Region.objects.get(autopark_id=int(car_data['region'])),
            city=City.objects.get(autopark_id=int(car_data['city_id'])),
            vin=car_data['cert_vin'],
            gearbox=Gearbox.objects.get(autopark_id=int(car_data['transmission'])),
            drive=Drive.objects.get(autopark_id=int(car_data['gear'])),
            fuel=Fuel.objects.get(autopark_id=int(car_data['fuel'])),
            engine_volume=float(car_data['capacity']),
            engine_power_hp=car_data['horsepower'],
            engine_power_kw=engine_power_kw,
            color=Color.objects.get(autopark_id=int(car_data['color'])),
            doors=int(car_data['cabin_doors']),
            seats=int(car_data['cabin_seats']),
            description=description
        )

        # for option_name in additional_info:
        #     new_car.options.add(Options.objects.get(name=option_name))

        for photo_url in photos:
            Photo.objects.create(car=new_car, url=f'https://autopark.ua{photo_url}')


# update models views
# class UpdateBodies(View):
#     def get(self, request, **kwargs):
#         if authenticate(request):
#             user = authenticate(request)[0]
#         else:
#             raise UserNotLoggedInException


