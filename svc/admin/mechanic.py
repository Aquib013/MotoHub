from django.contrib import admin


class MechanicAdmin(admin.ModelAdmin):
    list_display = ["mechanic_name", "place"]
    search_fields = ["mechanic_name"]
