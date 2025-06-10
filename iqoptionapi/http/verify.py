"""Module for IQ Option http verify resource."""

from iqoptionapi.http.resource import Resource


class Verify(Resource):
    """Class for IQ Option http verify resource."""
    # pylint: disable=too-few-public-methods

    url = "verify"

    def _post(self, data=None, headers=None):
        """Send post request for IQ Option API verify http resource.

        :returns: The instance of :class:`requests.Response`.
        """
        return self.api.send_http_request_v2(method="POST", url="https://auth.iqoption.com/api/v2/verify",
                                           data=data, headers=headers)

    def __call__(self, token, code):
        """Method to send verification code to IQ Option API.

        :param str token: The verification token received during login.
        :param str code: The verification code received via SMS.

        :returns: The instance of :class:`requests.Response`.
        """
        data = {
            "token": token,
            "code": code
        }

        return self._post(data=data)