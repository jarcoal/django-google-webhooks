from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import BaseFormView
from django.http import HttpResponse, JsonResponse

from .signals import webhook_received
from .forms import WebhookForm

class WebhookView(BaseFormView):
    """Catches webhooks from Google and triggers the notification signal"""

    form_class = WebhookForm
    http_method_names = ('post',)

    def form_valid(self, form):
        """Trigger webhook signal with webhook payload data."""

        # trigger signal
        webhook_received.send(sender=None, webhook_data={
            'message_number': form.cleaned_data['X_GOOG_MESSAGE_NUMBER'],
            'resource_state': form.cleaned_data['X_GOOG_RESOURCE_STATE'],
            'resource_id': form.cleaned_data['X_GOOG_RESOURCE_ID'],
            'resource_uri': form.cleaned_data['X_GOOG_RESOURCE_URI'],
            'channel_id': form.cleaned_data['X_GOOG_CHANNEL_ID'],
            'channel_expiration': form.cleaned_data['X_GOOG_CHANNEL_EXPIRATION'],
            'channel_token': form.cleaned_data['X_GOOG_CHANNEL_TOKEN'],
        })

        # let google know that we got the message
        return HttpResponse(200)

    def form_invalid(self, form):
        """Send back a 400 so that Google knows we failed"""
        return JsonResponse(form.errors, status=400)

    def get_form_kwargs(self):
        """Use the request headers instead of the post data"""
        kwargs = super(WebhookView, self).get_form_kwargs()
        kwargs['data'] = self.request.META
        return kwargs

    @method_decorator(csrf_exempt)
    def post(self, *args, **kwargs):
        """Disable CSRF"""
        return super(WebhookView, self).post(*args, **kwargs)
