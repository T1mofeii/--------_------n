from django.contrib import admin
from .models import CustomUser, Problem


admin.site.register(CustomUser)
admin.site.register(Problem)
