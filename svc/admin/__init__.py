from svc.admin.customer import *
from svc.admin.job import *
from svc.admin.vehicle import *
from svc.admin.service import *
from svc.admin.vendors import *
from svc.admin.items import *
from svc.admin.employee import *

from svc.models import Customer, Job, Vehicle, Service, Vendor, Item, Employee

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Employee, EmployeeAdmin)

