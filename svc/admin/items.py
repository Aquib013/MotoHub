from django.contrib import admin


class ItemAdmin(admin.ModelAdmin):
    list_display = ["item_name", "item_type", "item_quantity_in_stock"]
    search_fields = ["item_name"]
