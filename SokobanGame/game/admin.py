from django.contrib import admin
from .models import game_record

@admin.register(game_record)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'level', 'steps')  # 在后台列表中显示的字段