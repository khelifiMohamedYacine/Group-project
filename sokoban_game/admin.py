from django.contrib import admin


from .models import sokoban_results
admin.site.register(sokoban_results)

from .models import sokoban_level
admin.site.register(sokoban_level)
# Need to figure out this
