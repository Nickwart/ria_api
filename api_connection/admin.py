from django.contrib import admin
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
    Description,
    Options,
    Photo,
)


admin.site.register(Car)
admin.site.register(Categories)
admin.site.register(Body)
admin.site.register(Brand)
admin.site.register(CarModel)
admin.site.register(Currency)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(Gearbox)
admin.site.register(Drive)
admin.site.register(Fuel)
admin.site.register(Color)
admin.site.register(Description)
admin.site.register(Options)
admin.site.register(Photo)
