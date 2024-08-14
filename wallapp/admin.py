from django.contrib import admin
from wallapp.models import history,qanda,school

class historyadmin(admin.ModelAdmin):
    list_display= ('id'),
    search_fields=('id'),
    ordering = ('id'),

# Register your models here.
admin.site.register(history, historyadmin)
admin.site.register(qanda)
admin.site.register(school)