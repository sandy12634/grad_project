from django.contrib import admin
from .models import News, History, Service, Facility, Event

admin.site.register(News)
admin.site.register(History)
admin.site.register(Service)
admin.site.register(Facility)
admin.site.register(Event)