from django import template

register = template.Library()


@register.filter
def unique_vehicles(services):
    vehicles = set(service.vehicle for service in services)
    return list(vehicles)
