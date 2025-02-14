from django.contrib import admin
from .models import CustomUser, Problem

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Problem)
