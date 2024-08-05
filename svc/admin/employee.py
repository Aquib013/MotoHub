from django.contrib import admin


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["emp_name", "emp_contact"]
    search_fields = ["emp_name"]
