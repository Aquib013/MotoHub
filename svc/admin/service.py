from django.contrib import admin


class ServiceAdmin(admin.ModelAdmin):
    list_display = ["job", "service_type", "description", "vehicle"]
    search_fields = ["job", "vehicle", "description"]
