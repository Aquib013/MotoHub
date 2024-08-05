from svc.urls.accounts.signup import Signup_urlpatterns
from svc.urls.job.job import job_url_patterns
from svc.urls.customers.customers import customer_url_patterns
from svc.urls.vendor.vendor import vendor_url_patterns
from svc.urls.purchase_order.purchase_order import purchase_order_url_patterns
from svc.urls.item.item import item_url_patterns
from svc.urls.employee.employee import employee_url_patterns
from svc.urls.expense.expense import expense_urlpatterns

urlpatterns = []
urlpatterns += Signup_urlpatterns
urlpatterns += customer_url_patterns
urlpatterns += job_url_patterns
urlpatterns += vendor_url_patterns
urlpatterns += purchase_order_url_patterns
urlpatterns += item_url_patterns
urlpatterns += employee_url_patterns
urlpatterns += expense_urlpatterns



