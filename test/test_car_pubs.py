from ria_api.settings import RIA_API_KEY, RIA_USER_ID
import requests
from django.test import TestCase
from api_connection.models import Car

# url = f'https://developers.ria.com/auto/used/autos/?user_id={RIA_USER_ID}&api_key={RIA_API_KEY}'
# data = open("request.json")
# headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
# r = requests.post(url, data=data, headers=headers)

class LobbyUserTestCase(TestCase):
    def setUp(self):
        self.car = Car.objects.filter().all()
        print(self.car.values())
        # autopark_id = 25,
        # damage = True,
        # custom = True,
        # year = 2016,
        # price = 13000,
        # currency = self.currency,
        # category = self.category,
        # brand = self.brand,
        # model = self.car_model,
        # body = self.body,
        # mileage = 350000,
        # region = self.region,
        # city = self.city,
        # vin = 'JKBVNCB164A662141',
        # gearbox = self.gearbox,
        # drive = self.drive,
        # fuel = self.fuel,
        # consumption_city = 10,
        # consumption_route = 8,
        # consumption_combine = 9,
        # engine_volume = 1.5,
        # engine_power_hp = 105,
        # engine_power_kw = 79.0442,
        # color = self.color,
        # metallic_color = True,
        # auctions = True,
        # comments_allowed = True,
        # comments_check = False,
        # video = 'lLEiT9PeHSg',
        # doors = 5,
        # seats = 5,
        # country = self.country,
        # spareParts = False,

    def test_model_instances_creates(self):
        assert False
        # self.assertEqual(Car.objects.get(autopark_id=25), self.car)

