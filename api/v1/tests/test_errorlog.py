from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class ErrorLogTestCase(APITestCase):
    def test_user_authenticated(self):
        r = self.client.post(reverse('api:v1:error-log'), {
            'header': 'Error',
            'message': '''Something really bad happened.
And no traces.'''
        })
        self.assertEqual(r.status_code, 201)
