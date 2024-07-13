from django.contrib import admin


class VehicleAdmin(admin.ModelAdmin):
    list_display = ["name", "make"]
    search_fields = ["name"]
