from django.contrib import admin

# Register your models here.
from .models import Quiz, Question, TrueFalse

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(TrueFalse)
