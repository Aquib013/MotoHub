from django.contrib import admin


class JobAdmin(admin.ModelAdmin):
    list_display = ["customer", "created_at"]
    search_fields = ["customer"]
