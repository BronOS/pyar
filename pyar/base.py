"""
    Base PyAR package.
    ~~~~~~~~~~~~~~~~~~

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


from .exception import AdapterTypeException, AdapterNotExistsException, ModelNotExistsException


class PyAR(object):
    """Base python active record class."""

    __models = dict()
    "PyAR models."

    __adapters = dict()
    "PyAR adapters."

    @classmethod
    def add_adapter(cls, adapter, name=None):
        """Adds new adapter. If name is not specified it adds adapter as default.

        :param adapter: PyAR adapter obj.
        :type: IAdapter
        :param name: Adapter name.
        :type name: str
        :rtype: None
        """
        if not isinstance(adapter, IAdapter):
            raise AdapterTypeException('Adapter must be an instance of IAdapter.')

        cls.__adapters[name] = adapter

    @classmethod
    def get_adapter(cls, name=None):
        """Returns adapter.

        :param name: Adapter name.
        :type name: str
        :rtype: IAdapter
        """
        if not name in cls.__adapters:
            raise AdapterNotExistsException('Adapter [%s] does not exists.' % name)

        return cls.__adapters[name]

    @classmethod
    def get_models(cls):
        """Returns all registered models.

        :rtype: dict
        """
        return cls.__models

    @classmethod
    def get_model(cls, model_name):
        """Returns registered model.

        :rtype: IModel
        """
        if model_name not in cls.__models:
            raise ModelNotExistsException('Model [%s] not exists.')

        return cls.__models[model_name]

    @classmethod
    def add_model(cls, model_cls):
        """Register model.

        :rtype: None
        """
        cls.__models[model_cls.__name__] = model_cls


from .adapter import IAdapter