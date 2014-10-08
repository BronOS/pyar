"""
    PyAR JIRA reader adapter package.
    ~~~~~~~~~~~~~~~~~~~~~

    :license:
        This code is a part of Communication Interface for Import/Export,
        which is a proprietary subject of its rightful owners. Any form of
        copy or distribution is forbidden without written permission.

    :copyright:
        Copyright (c) 2014 symmetrics - a CGI Group brand

    :author:
        symmetrics - a CGI Group brand <info@symmetrics.de>
        Oleg Bronzov <oleg.bronzov@symmetrics.de>
"""

from ..adapter import AAdapter
from ..model import ModelData
from ..exception import AdapterExecuteException

import requests


class _AUrl(AAdapter):
    """JIRA adapter url helper."""

    def get_url(self, resource, params):
        """Returns JIRAs url.

        :param resource: Resource name.
        :type resource: str
        :param params: Url params.
        :type params: dict
        :rtype:
        """
        url = self.__add_last_slash(
            self.__add_last_slash(self.get_config('host')) + resource if resource[0] != '/' else resource[1:]
        )

        if len(params):
            url += '?' + '&'.join([str(key) + '=' + str(value) for key, value in params.items()])

        return url

    @staticmethod
    def __add_last_slash(url):
        """Adds slash to the end of the url.

        :param url: JIRA url.
        :type url: str
        :rtype: str
        """
        return url + '/' if url[-1:] != '/' else url


class JiraReaderAdapter(_AUrl):
    """PyAR JIRA adapter."""

    def __init__(self, host, user=None, passwd=None, verify=False):
        """Constructor. Sets adapter config.

        :param host: Host path.
        :type host: str
        :param user: User name.
        :type user: str
        :param passwd: User password.
        :type passwd: str
        :param verify: Shows whether requests lib will be verify host.
        :type verify: bool
        """
        self.__last_response = None
        super().__init__(host=host, user=user, passwd=passwd, verify=verify)

    def read(self, model_cls, **kwargs):
        """Reads from jira with received parameters.

        :param model_cls: PyAR model class.
        :type model_cls: ModelData
        :rtype: list
        """
        params = {
            'verify': self.get_config('verify')
        }
        if self.has_config('user'):
            params['auth'] = (
                self.get_config('user'),
                self.get_config('passwd')
            )

        self.__last_response = requests.get(
            self.get_url(model_cls.get_resource(), kwargs),
            **params
        )

        ret = []

        if self.__last_response.status_code == 200:
            result = self.__last_response.json()
            if isinstance(result, dict):
                result = [result]

            for item in result:
                ret.append(model_cls(item, False))
        else:
            raise AdapterExecuteException('Can\'t read data. Status code: %s' % self.__last_response.status_code)

        return ret

    def get_last_response(self):
        """Returns last response.

        :rtype: Response
        """
        return self.__last_response