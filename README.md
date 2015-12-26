# django-google-webhooks
Django views for working with Google API webhooks

## Installation

Install with pip:
```bash
pip install django-google-webhooks
```

Add to `INSTALLED_APPS`:
```python
INSTALLED_APPS = (
  # ...
  'google_webhooks',
)
```

Add to `urlpatterns`:
```python
urlpatterns = [
  # ...
  url(r'^google-webhooks/', include('google_webhooks.urls')),
]
```

## Usage

Listen for the `webhook_received` signal:

```python
from django.dispatch import receiver
from google_webhooks.signals import webhook_received

@receiver(webhook_received, dispatch_uid='do_something')
def do_something(sender, webhook_data, **kwargs):
  """
  Do something with the Google webhook data.
  
  {
    # Will always be present
    "channel_id": "4ba78bf0-6a47-11e2-bcfd-0800200c9a66",
    "resource_state": "update",
    "resource_id": "ret08u3rv24htgh289g",
    "resource_uri": "https://www.googleapis.com/drive/v3/files/ret08u3rv24htgh289g",
    "message_number": 1,
    
    # Optional
    "channel_expiration": datetime(2015, 1, 1, ...),
    "channel_token": "398348u3tu83ut8uu38",
  }
  """
```
