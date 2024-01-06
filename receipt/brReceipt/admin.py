from django.contrib import admin
from .models import Category
from .models import Receipt
from .models import RatesReceipt

# Register your models here.
admin.site.register(Category)
admin.site.register(Receipt)
admin.site.register(RatesReceipt)