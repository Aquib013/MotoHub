from django.contrib import admin


class ServiceAdmin(admin.ModelAdmin):
    list_display = ["job", "name", "service_type", "vehicle"]
    search_fields = ["job", "vehicle", "name"]
