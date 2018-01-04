#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'xiwei'

import requests
from util.logger import log


class ServerError(Exception):
    def __init__(self, status, message):
        self.status = status
        self.message = message


class NgAlertD(object):
    _host = 'http://localhost:9757'

    def __init__(self, username=None, password=None, client_id=None, token=None):
        self.username = username
        self.password = password
        self.client_id = client_id
        self.token = token

    def _request(self, url, params=None, data=None):
        _url = f'{self._host}/{url}'
        try:
            if data:
                res = requests.post(_url, params, data)
            else:
                res = requests.get(_url, params)
            res.raise_for_status()
            res = res.json()
        except requests.HTTPError as he:
            log.error(f'Server response Error: {he.response.text}')
            return None
        else:
            if res.get('status') != 200:
                raise ServerError(res.get('status'), res.get('error'))
            return res.get('result')

    def is_login(self):
        print(self.account_info())

    def account_login(self):
        return self._request(
            'account/login',
            data={
                "username": self.username,
                "password": self.password
            }
        )

    def account_info(self):
        return self._request(
            'account/info',
            data={
                "token": self.token
            }
        )


if __name__ == '__main__':
    NgAlertD().account_info()
