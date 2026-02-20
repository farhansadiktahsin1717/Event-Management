from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "date", "time", "location")
    search_fields = ("name", "location")
    list_filter = ("category", "date")
