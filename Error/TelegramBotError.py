import json
from pyodata.exceptions import HttpError


def json_get(obj, member, default=None):
    # if not isinstance(obj, dict):
    #     raise ValueError('Это не JSON')

    value = obj.get(member, default)
    return value


class TelegramBotError(HttpError):
    def __init__(self, message, response):
        error_details = []

        message = ''

        data = json.loads(response.content.decode("utf-8"))

        error = json_get(data, 'error', {})
        inner_error = json_get(error, 'innererror', {})

        message = json_get(json_get(error, 'message', {}),
                           'value', message)

        # error_details = [json_get(detail, 'message', ''),
        #                  for detail
        #                  in json_get(inner_error, 'errordetails', [])]

        super(TelegramBotError, self).__init__(message, response)
        # self.error_details = error_details

HttpError.VendorType = TelegramBotError
