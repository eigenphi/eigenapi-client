import requests


class StatusApi(object):
    def __init__(self, host: str = 'api.eigenapi.io'):
        self.host = "https://" + host
        self.endpoint = 'status'

    def do_request(self):
        url = f"{self.host}/{self.endpoint}"

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers)
        response_result = response.json()
        status_result = {}
        if response.status_code == 200:
            if 'errcode' in response_result:
                raise Exception(response_result['errcode'], response_result['err'])
            elif 'data' in response_result:
                status_result = response_result['data']

        elif response.status_code == 401 or response.status_code == 419:
            raise Exception(response_result['errcode'], response_result['err'])
        else:
            raise Exception(response.status_code, response.reason)

        return status_result
