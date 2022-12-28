from django.db import models


class Categories(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=25)
    ria_id = models.IntegerField()


# Типи кузова
class Body(models.Model):
    objects = models.Manager()
    # category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    ria_id = models.IntegerField()


class Brand(models.Model):
    objects = models.Manager()
    # category = models.ManyToManyField(Categories)
    name = models.CharField(max_length=25)
    ria_id = models.IntegerField()


class CarModel(models.Model):
    objects = models.Manager()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    ria_id = models.IntegerField()


class Currency(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=25)
    ria_id = models.IntegerField()


class Region(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=25)
    ria_id = models.IntegerField()


class City(models.Model):
    objects = models.Manager()
    # region = models.ForeignKey(Categories, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    ria_id = models.IntegerField()


class Gearbox(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=25)
    ria_id = models.IntegerField()


# тип приводу
class Drive(models.Model):
    objects = models.Manager()
    # category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    ria_id = models.IntegerField()


class Fuel(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=25)
    ria_id = models.IntegerField()


class Color(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=25)
    ria_id = models.IntegerField()


class Country(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=25)
    ria_id = models.IntegerField()


class Car(models.Model):
    #    \"modification\":\"V12 AMG B-turbo\", ЩО РОБИТИ З МОДИФІКАЦІЯМИ????
    objects = models.Manager()

    autopark_id = models.CharField(blank=False, max_length=50)
    damage = models.BooleanField(default=False, blank=True)
    # Чи розмитнена машина
    custom = models.BooleanField(default=True, blank=True)
    year = models.IntegerField(blank=False)
    price = models.IntegerField(blank=False)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='price_currency')
    # тип транспорту
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    # # like verbose name
    # modification = models.CharField(max_length=35)
    # тип кузова
    body = models.ForeignKey(Body, on_delete=models.CASCADE)
    mileage = models.IntegerField(blank=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    vin = models.CharField(blank=False, max_length=25)
    gearbox = models.ForeignKey(Gearbox, on_delete=models.CASCADE)
    drive = models.ForeignKey(Drive, on_delete=models.CASCADE)
    fuel = models.ForeignKey(Fuel, on_delete=models.CASCADE)
    consumption_city = models.FloatField(blank=True)
    consumption_route = models.FloatField(blank=True)
    consumption_combine = models.FloatField(blank=True)
    engine_volume = models.FloatField(blank=True)
    # кінські сили
    engine_power_hp = models.IntegerField(blank=True)
    engine_power_kw = models.IntegerField(blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    metallic_color = models.BooleanField(blank=True)
    # дозволити торги під оголошенням
    auctions = models.BooleanField(default=True)
    comments_allowed = models.BooleanField(default=True)
    comments_check = models.BooleanField(default=False)
    # YouTube video key (like this "lLEiT9PeHSg")
    video = models.CharField(blank=True, max_length=50)
    doors = models.IntegerField(blank=True)
    seats = models.IntegerField(blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    # переіменувати і зробити міграції
    spareParts = models.BooleanField(default=False, blank=True)


class Description(models.Model):
    objects = models.Manager()
    car = models.OneToOneField(to=Car, on_delete=models.CASCADE)
    ua = models.CharField(max_length=2000)
    ru = models.CharField(max_length=2000)


# request example
#
# curl -X POST "https://developers.ria.com/auto/used/autos/?user_id=7069830&api_key=YOUR_API_KEY" -H "accept: application/json" -H "content-type: application/json" -d
# "{
#    \"damage\":false,
#    \"custom\":false,
#    \"year\":2016,
#    \"price\":{
#       \"value\":80000,
#       \"currency\":{
#          \"id\":1
#       }
#    },
#    \"categories\":{
#       \"main\":{
#          \"id\":1
#       }
#    },
#    \"brand\":{
#       \"id\":5
#    },
#    \"model\":{
#       \"id\":963
#    },
#    \"modification\":\"V12 AMG B-turbo\",
#    \"body\":{
#       \"id\":6
#    },
#    \"mileage\":32,
#    \"region\":{
#       \"id\":10
#    },
#    \"city\":{
#       \"id\":10
#    },
#    \"VIN\":\"JKBVNCB164A662141\",
#    \"gearbox\":{
#       \"id\":1
#    },
#    \"drive\":{
#       \"id\":2
#    },
#    \"fuel\":{
#       \"id\":2,
#       \"consumption\":{
#          \"city\":10,
#          \"route\":6,
#          \"combine\":8
#       }
#    },
#    \"engine\":{
#       \"volume\":{
#          \"liters\":3.5
#       }
#    },
#    \"power\":{
#       \"hp\":585,
#       \"kW\":430
#    },
#    \"color\":{
#       \"id\":10,
#       \"metallic\":true
#    },
#    \"post\":{
#       \"auctions\":true,
#       \"comments\":{
#          \"allowed\":true,
#          \"check\":false
#       },
#       \"exchanges\":{
#          \"payment\":{
#             \"id\":2
#          },
#          \"type\":{
#             \"id\":1
#          }
#       }
#    },
#    \"video\":{
#       \"key\":\"lLEiT9PeHSg\"
#    },
#    \"description\":{
#       \"ru\":\"Авто в идеальном состоянии,
#       вложений не требует\",
#       \"uk\":\"Авто в ідеальному стані,
#       вкладень не потребує\"
#    },
#    \"doors\":2,
#    \"seats\":2,
#    \"country\":{
#       \"import\":{
#          \"id\":0
#       }
#    },
#    \"spareParts\":false
# } "

#   response example
# {
#    "damage":false,
#    "custom":false,
#    "year":2016,
#    "price":{
#       "value":80000,
#       "currency":{
#          "id":1
#       }
#    },
#    "categories":{
#       "main":{
#          "id":1
#       },
#       "all":[
#          {
#             "id":1
#          }
#       ]
#    },
#    "brand":{
#       "id":5
#    },
#    "model":{
#       "id":963
#    },
#    "modification":"V12 AMG B-turbo",
#    "body":{
#       "id":6
#    },
#    "mileage":32,
#    "region":{
#       "id":10
#    },
#    "city":{
#       "id":10
#    },
#    "VIN":"JKBVNCB164A66XXXX",
#    "gearbox":{
#       "id":1
#    },
#    "drive":{
#       "id":2
#    },
#    "fuel":{
#       "id":2,
#       "consumption":{
#          "city":10,
#          "route":6,
#          "combine":8
#       }
#    },
#    "engine":{
#       "volume":{
#          "liters":3.5
#       }
#    },
#    "power":{
#       "hp":585,
#       "kW":430
#    },
#    "color":{
#       "id":10,
#       "metallic":true
#    },
#    "post":{
#       "auctions":true,
#       "comments":{
#          "allowed":true,
#          "check":false
#       },
#       "exchanges":{
#          "payment":{
#             "id":2
#          },
#          "type":{
#             "id":1
#          }
#       }
#    },
#    "video":{
#       "key":"lLEiT9PeHSg"
#    },
#    "description":{
#       "ru":"Авто в идеальном состоянии, вложений не требует",
#       "uk":"Авто в ідеальному стані, вкладень не потребує"
#    },
#    "doors":2,
#    "seats":2,
#    "country":{
#       "import":{
#          "id":0
#       }
#    },
#    "spareParts":false,
#    "user":{
#       "id":7069830
#    },
#    "ip":"80.91.174.90",
#    "dates":{
#       "created":"2017-09-18T12:07:43.840Z"
#    },
#    "status":{
#       "id":13
#    },
#    "_id":20476120
# }
