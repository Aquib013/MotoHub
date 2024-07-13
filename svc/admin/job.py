from django.contrib import admin


class JobAdmin(admin.ModelAdmin):
    list_display = ["mechanic", "created_at"]
    search_fields = ["mechanic"]
