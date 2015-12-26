from django import forms
from datetime import datetime

class UnixDateTimeField(forms.DateTimeField):
    """Custom form field for parsing unix timestamps into datetimes"""

    def to_python(self, value):
        if not isinstance(value, (str, float)):
            return super(UnixDateTimeField, self).to_python(value)

        return datetime.fromtimestamp(value)

class WebhookForm(forms.Form):
    """Used for validating the Google notification"""

    X_GOOG_MESSAGE_NUMBER = forms.IntegerField()
    X_GOOG_CHANNEL_ID = forms.CharField()
    X_GOOG_CHANNEL_EXPIRATION = UnixDateTimeField(required=False)
    X_GOOG_CHANNEL_TOKEN = forms.CharField(required=False)
    X_GOOG_RESOURCE_STATE = forms.CharField()
    X_GOOG_RESOURCE_ID = forms.CharField()
    X_GOOG_RESOURCE_URI = forms.CharField()
