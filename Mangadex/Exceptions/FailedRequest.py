import requests 
import logging
import json

class FailedRequest(Exception):

    def __init__(self, response:requests.Response):
        self.response = response

    def dump_request_information(self, logger:logging)->None:
        response_information = {'Response Url': self.response.url, 
                'Status Code': self.response.status_code, 
                'Headers': self.response.headers
                }

        logger.error(json.dumps(response_information, indent=4))
