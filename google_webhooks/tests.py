from django.test import TestCase
from django.core.urlresolvers import reverse_lazy
from .signals import webhook_received
from datetime import datetime
from time import mktime

webhook_url = reverse_lazy('google_webhook')

TEST_CHANNEL_ID = 'channel_id'
TEST_CHANNEL_TOKEN = 'hello=world'
TEST_CHANNEL_EXPIRATION = datetime(2015, 1, 1)
TEST_MESSAGE_NUMBER = 1
TEST_RESOURCE_STATE = 'sync'
TEST_RESOURCE_ID = 'resource_id'
TEST_RESOURCE_URI = 'resource_uri'


class TestWebhooks(TestCase):
    """"""

    def test_valid_webhook(self):
        # if this isn't toggled to true by the signal, the test fails
        self.signal_fired = False

        def check_signal_data(sender, webhook_data, **kwargs):
            self.assertEqual(webhook_data['resource_state'], TEST_RESOURCE_STATE)
            self.assertEqual(webhook_data['channel_id'], TEST_CHANNEL_ID)
            self.assertEqual(webhook_data['message_number'], TEST_MESSAGE_NUMBER)
            self.assertEqual(webhook_data['resource_id'], TEST_RESOURCE_ID)
            self.assertEqual(webhook_data['resource_uri'], TEST_RESOURCE_URI)
            self.assertEqual(webhook_data['channel_token'], TEST_CHANNEL_TOKEN)
            self.assertEqual(webhook_data['channel_expiration'],
                TEST_CHANNEL_EXPIRATION)

            # note that this hook fired
            self.signal_fired = True

        webhook_received.connect(check_signal_data)

        resp = self.client.post(webhook_url, {},
            X_GOOG_RESOURCE_STATE=TEST_RESOURCE_STATE,
            X_GOOG_CHANNEL_ID=TEST_CHANNEL_ID,
            X_GOOG_MESSAGE_NUMBER=TEST_MESSAGE_NUMBER,
            X_GOOG_RESOURCE_ID=TEST_RESOURCE_ID,
            X_GOOG_RESOURCE_URI=TEST_RESOURCE_URI,
            X_GOOG_CHANNEL_EXPIRATION=mktime(TEST_CHANNEL_EXPIRATION.timetuple()),
            X_GOOG_CHANNEL_TOKEN=TEST_CHANNEL_TOKEN,
        )
        self.assertEqual(resp.status_code, 200)

        # make sure the signal fired
        self.assertTrue(self.signal_fired)
