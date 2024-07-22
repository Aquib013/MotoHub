from django.contrib import admin


class CustomerAdmin(admin.ModelAdmin):
    list_display = ["customer_name", "place", "dues"]
    search_fields = ["customer_name"]
