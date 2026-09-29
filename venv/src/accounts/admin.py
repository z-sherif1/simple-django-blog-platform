from django.contrib import admin
from .models import Profile,Post,Comment,Category
# Register your models here.
admin.site.register([Profile,Post,Comment,Category])
