"""
    PyAR adapter package.
    ~~~~~~~~~~~~~~~~~~~~~

    :license:
        This code is a part of Communication Interface for Import/Export,
        which is a proprietary subject of its rightful owners. Any form of
        copy or distribution is forbidden without written permission.

    :copyright:
        Copyright (c) 2014 symmetrics - a CGI Group brand

    :author:
        symmetrics - a CGI Group brand <info@symmetrics.de>
        Oleg Bronzov <oleg.bronzov@symmetrics.de>,
"""


from .exception import AdapterConfigKeyException, ModelTypeException
from .model import IModel


class IAdapter(object):
    """Adapter interface."""

    def read(self, model, **kwargs):
        """Read method.

        :rtype: list
        """
        pass

    def create(self, model, **kwargs):
        """Create model.

        :rtype: bool
        """
        pass

    def update(self, model, **kwargs):
        """Update model.

        :rtype: bool
        """
        pass

    def delete(self, model, **kwargs):
        """Delete model.

        :rtype: bool
        """
        pass


class _AConfig(object):
    """Adapter config abstract class."""

    def __init__(self, **kwargs):
        """Constructor.
        Sets adapter config.
        """
        self.__config = dict()
        for key, value in kwargs.items():
            self.add_config(key, value)

    def add_config(self, key, value):
        """Sets configs key ~> value pair.
        Will replace old value if it already exists.

        :param key: Config key.
        :type key: str
        :param value: Config value.
        :type value: str
        :rtype: None
        """
        self.__config[key] = value

    def get_config(self, key=None):
        """Returns configs value if key is specified and all config dict otherwise.

        :param key: Config key.
        :type key: str
        :rtype: str|dict
        """
        if key is not None and key not in self.__config:
            raise AdapterConfigKeyException('Config key [%s] does not exists.' % key)

        return self.__config if key is None else self.__config[key]

    def rm_config(self, key):
        """Removes configs value by key and returns removed value.

        :param key: Config key.
        :type key: str
        :rtype: str
        """
        if key not in self.__config:
            raise AdapterConfigKeyException('Config key [%s] does not exists.' % key)

        return self.__config.pop(key)

    def clear_config(self):
        """Removes all items from config.

        :rtype: None
        """
        self.__config = dict()


class AAdapter(_AConfig, IAdapter):
    """Abstract adapter class."""

    def __init__(self, **kwargs):
        """Constructor.
        Sets adapter's config.
        """
        super().__init__(**kwargs)

    @staticmethod
    def __check_model_type(model):
        """Checks model type.

        :param model: Methods model.
        :type model: IModel
        :rtype: None
        """
        if not isinstance(model, IModel):
            raise ModelTypeException('Model must be an instance of IModel')

    def read(self, model, **kwargs):
        """Read method.

        :rtype: list
        """
        self.__check_model_type(model)

    def create(self, model, **kwargs):
        """Create model.

        :rtype: bool
        """
        self.__check_model_type(model)

    def update(self, model, **kwargs):
        """Update model.

        :rtype: bool
        """
        self.__check_model_type(model)

    def delete(self, model, **kwargs):
        """Delete model.

        :rtype: bool
        """
        self.__check_model_type(model)
