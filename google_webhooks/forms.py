from django import forms
from datetime import datetime

RESOURCE_STATES = (
    ('sync', 'sync'),
    ('exists', 'exists'),
    ('not_exists', 'not_exists'),
)

class UnixDateTimeField(forms.DateTimeField):
    """Custom form field for parsing unix timestamps into datetimes"""

    def to_python(self, value):
        return datetime.fromtimestamp(value)

class WebhookForm(forms.Form):
    """Used for validating the Google notification"""

    X_GOOG_MESSAGE_NUMBER = forms.IntegerField()
    X_GOOG_CHANNEL_ID = forms.CharField()
    X_GOOG_CHANNEL_EXPIRATION = UnixDateTimeField(required=True)
    X_GOOG_CHANNEL_TOKEN = forms.CharField(required=False)
    X_GOOG_RESOURCE_STATE = forms.ChoiceField(choices=RESOURCE_STATES)
    X_GOOG_RESOURCE_ID = forms.CharField()
    X_GOOG_RESOURCE_URI = forms.CharField()
