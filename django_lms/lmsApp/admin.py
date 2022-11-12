from django.contrib import admin
from lmsApp import models
from .models import Books,Category,SubCategory,Members,Borrow,Chat
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User 
# Register your models here.
# admin.site.register(models.Groups)
admin.site.register(Books)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Members)
admin.site.register(Borrow)
admin.site.register(User)
admin.site.register(Chat)