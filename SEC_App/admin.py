from django.contrib import admin
from .models import Request, Tweet, Analysis
# Register your models here.
admin.site.register(Request)
admin.site.register(Tweet)
admin.site.register(Analysis)