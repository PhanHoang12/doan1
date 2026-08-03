from django.contrib import admin

# Register your models here.
from .models import Country

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name')
admin.site.register(Country)
