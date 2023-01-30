from django.db import models


class Categories(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=25)
    ria_id = models.IntegerField(unique=True)
    autopark_id = models.IntegerField(unique=True)


class Brand(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=25, unique=True)
    ria_id = models.IntegerField(unique=True)
    autopark_id = models.IntegerField(unique=True)


class CarModel(models.Model):
    objects = models.Manager()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, unique=True)
    ria_id = models.IntegerField()
    autopark_id = models.IntegerField()


# Типи кузова
class Body(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=25, unique=True)
    ria_id = models.IntegerField(unique=True)
    autopark_id = models.IntegerField(unique=True)


class Currency(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=25, unique=True)
    ria_id = models.IntegerField(unique=True)
    autopark_id = models.IntegerField(unique=True)


class Region(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=25, unique=True)
    ria_id = models.IntegerField(unique=True)
    autopark_id = models.IntegerField(unique=True)


class City(models.Model):
    objects = models.Manager()
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, unique=True)
    ria_id = models.IntegerField()
    autopark_id = models.IntegerField()


class Gearbox(models.Model):
    objects = models.Manager()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, unique=True)
    ria_id = models.IntegerField(unique=True)
    autopark_id = models.IntegerField(unique=True)


# тип приводу
class Drive(models.Model):
    objects = models.Manager()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, unique=True)
    ria_id = models.IntegerField(unique=True)
    autopark_id = models.IntegerField(unique=True)


class Fuel(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=25, unique=True)
    ria_id = models.IntegerField(unique=True)
    autopark_id = models.IntegerField(unique=True)


class Color(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=25, unique=True)
    ria_id = models.IntegerField(unique=True)
    autopark_id = models.IntegerField(unique=True)


class Description(models.Model):
    objects = models.Manager()
    ua = models.CharField(max_length=2000)
    ru = models.CharField(max_length=2000)


class Options(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=55, unique=True),
    ria_id = models.IntegerField(unique=True)


class Car(models.Model):
    objects = models.Manager()

    autopark_id = models.CharField(blank=False, max_length=50)
    # Чи розмитнена машина
    custom = models.BooleanField(default=True, blank=True)
    year = models.IntegerField(blank=False)
    price = models.IntegerField(blank=False)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='price_currency')
    # тип транспорту
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    modification = models.CharField(max_length=35)
    # тип кузова
    body = models.ForeignKey(Body, on_delete=models.CASCADE)
    mileage = models.IntegerField(blank=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    vin = models.CharField(blank=False, max_length=25, unique=True)
    gearbox = models.ForeignKey(Gearbox, on_delete=models.CASCADE)
    drive = models.ForeignKey(Drive, on_delete=models.CASCADE)
    fuel = models.ForeignKey(Fuel, on_delete=models.CASCADE)
    engine_volume = models.FloatField(blank=True)
    engine_power_hp = models.IntegerField(blank=True)
    engine_power_kw = models.IntegerField(blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    # дозволити торги під оголошенням
    auctions = models.BooleanField(default=True)
    comments_allowed = models.BooleanField(default=True)
    comments_check = models.BooleanField(default=False)
    video = models.CharField(blank=True, max_length=50)
    doors = models.IntegerField(blank=True)
    seats = models.IntegerField(blank=True)
    spare_parts = models.BooleanField(default=False, blank=True)
    description = models.OneToOneField(to=Description, on_delete=models.CASCADE, blank=True, null=True)
    options = models.ManyToManyField(Options, related_name='options')


class Photo(models.Model):
    objects = models.Manager()
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    url = models.CharField(max_length=100, unique=True)


class EventCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    category_description = models.CharField(max_length=255)


class Log(models.Model):
    objects = models.Manager()
    car_id = models.IntegerField()
    date = models.DateTimeField()
    event_category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    event_description = models.CharField(max_length=255)


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
