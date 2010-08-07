from orders.models import Order


def current_order(request):
    """Returns the active order from the session (creates one if necessary)."""
    return {'current_order': Order.get_or_create(request)}
