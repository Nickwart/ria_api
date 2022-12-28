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
    Country,
    Description
)


class GetCarView(View):
    def get(self, request):
        # data = request.data
        car = Car.objects.get(id=1)
        print(car.__dict__)
        print(car.brand_id)
        url = f'https://developers.ria.com/auto/used/autos/?user_id={RIA_USER_ID}&api_key={RIA_API_KEY}'
        data = {
            "damage": car.damage,
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
            "modification": "V12 AMG B-turbo",
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
            "VIN": 'JKBVNCB164A662141',
            "gearbox": {
                "id": car.gearbox.ria_id
            },
            "drive": {
                "id": car.drive.ria_id
            },
            "fuel": {
                "id": car.fuel.ria_id,
                "consumption": {
                    "city": car.consumption_city,
                    "route": car.consumption_route,
                    "combine": car.consumption_combine
                }
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
                "metallic": car.metallic_color
            },
            "post": {
                "auctions": False,
                "comments": {
                    "allowed": True,
                    "check": False
                },
                "exchanges": {
                    "payment": {
                        "id": 2
                    },
                    "type": {
                        "id": 1
                    },
                }
            },
            "video": {
                "key": car.video
            },
            "description": {
                "ru": "заглушка для опису",
                "uk": "заглушка для опису"

            },
            "doors": car.doors,
            "seats": car.seats,
            "country": {
                "import": {
                    "id": car.country.ria_id
                }
            },
            "spareParts": car.spareParts
        }
        print(data)
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        response = requests.post(url, data=json.dumps(data), headers=headers)

        return HttpResponse(response, status=200)


# update models views

# class UpdateBodies(View):
#     def get(self, request, **kwargs):
#         if authenticate(request):
#             user = authenticate(request)[0]
#             if user.is_staff or user.is_superuser:
#                 all_lobby = Lobby.objects.all().filter(**kwargs)
#                 return HttpResponse(all_lobby, status=200)
#             else:
#                 all_lobby = Lobby.objects.all().filter(private=False, **kwargs)
#                 return HttpResponse(all_lobby, status=200)
#         else:
#             raise UserNotLoggedInException


