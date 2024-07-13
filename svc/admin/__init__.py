from svc.admin.mechanic import *
from svc.admin.job import *
from svc.admin.vehicle import *
from svc.admin.service import *
from svc.admin.vendors import *
from svc.admin.items import *

from svc.models import Mechanic, Job, Vehicle, Service, Vendor, Item


admin.site.register(Mechanic, MechanicAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Item, ItemAdmin)
