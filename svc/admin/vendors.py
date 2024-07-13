from django.contrib import admin


class VendorAdmin(admin.ModelAdmin):
    list_display = ["vendor_name"]
    search_fields = ["vendor_name"]
