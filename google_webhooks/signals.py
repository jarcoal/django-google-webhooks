from django.dispatch import Signal

# Triggered when a new Google webhook is received by the dispatch view.
webhook_received = Signal(providing_args=['webhook_data'])