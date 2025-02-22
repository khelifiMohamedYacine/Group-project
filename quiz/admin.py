from django.contrib import admin

# Register your models here.
from .models import Quiz, TrueFalse
admin.site.register(Quiz)
admin.site.register(TrueFalse)
