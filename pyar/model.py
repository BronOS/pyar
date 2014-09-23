"""
    PyAR model package.
    ~~~~~~~~~~~~~~~~~~~

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


import re

from .base import PyAR

from .exception import ModelFieldNameException


class IModelData(object):
    """Model data interface."""

    def set_data(self, data):
        """Sets models data.

        :param data: Models data.
        :type data: dict
        :rtype: None
        """
        pass

    def get_data(self, with_models=True):
        """Returns models data.

        :param with_models: Adds information about nested models to the dict.
        :type with_models: bool
        :rtype: dict
        """
        pass

    def get_data_models(self):
        """Returns dict of model's fields of this model.

        :rtype: dict
        """
        pass

    def get_origin_data(self):
        """Returns models origin data.

        :rtype: dict
        """
        pass

    def to_dict(self, with_models=True):
        """Returns dict representation of model.

        :param with_models: Adds information about nested models to the dict.
        :type with_models: bool
        :rtype: dict
        """
        pass


class IModelAdapter(object):
    """Model adapter interface."""

    @classmethod
    def get_read_adapter(cls):
        """Returns models read adapter name.

        :rtype: str
        """
        pass

    @classmethod
    def get_write_adapter(cls):
        """Returns models write adapter name.

        :rtype: str
        """
        pass

    @classmethod
    def find(cls, **kwargs):
        """Find entities and returns it as list of models.

        :rtype: list
        """
        pass

    @classmethod
    def find_one(cls, **kwargs):
        """Returns firs element of found entities.

        :rtype: IModel|None
        """
        pass

    def create(self, **kwargs):
        """Creates model.

        :rtype: bool
        """
        pass

    def update(self, **kwargs):
        """Updates model.

        :rtype: bool
        """
        pass

    def delete(self, **kwargs):
        """Deletes model.

        :rtype: bool
        """
        pass

    def save(self, **kwargs):
        """Saves model.

        :rtype: bool
        """
        pass


class IModelNew(object):
    """Is model new interface."""

    def is_new(self):
        """Returns whether this model is new.

        :rtype: bool
        """
        pass

    def set_is_new(self, value):
        """Sets is new state for model.

        :param value: Value of state.
        :type value: bool
        :rtype: None
        """
        pass


class IModel(IModelAdapter, IModelData, IModelNew):
    """PyAR model interface."""

    @classmethod
    def get_resource(cls):
        """Returns models resource name.

        :rtype: str
        """
        pass


class AModelData(IModelData, IModelNew):
    """Provides interfaces to work with data."""

    def __init__(self, data=None):
        """Sets data into model.

        :param data: Models data.
        :type data: dict
        """
        self.__origin_data = dict()
        self.__data = dict()

        if isinstance(data, dict):
            self.__origin_data = data
            self.set_data(data)

        super().__init__()

    def set_data(self, data):
        """Sets models data.
        Replace all old value.

        :param data: Models data.
        :type data: dict
        :rtype: None
        """
        for key, value in data.items():
            if key[0] == '_':
                raise ModelFieldNameException('Invalid field name [%s]' % key)
            setattr(self, key, value)

    def get_data_models(self):
        """Returns dict of model's fields of this model.

        :rtype: dict
        """
        ret = dict()

        for key, value in self.__dict__.items():
            if isinstance(value, IModel):
                ret[key] = value

        return ret

    def get_data(self, with_models=True):
        """Returns models data.

        :param with_models: Adds information about nested models to the dict.
        :type with_models: bool
        :rtype: dict
        """
        ret = self.__data

        if with_models:
            ret.update(self.get_data_models())

        return ret

    def get_origin_data(self):
        """Returns models origin data.

        :rtype: dict
        """
        return self.__origin_data

    def to_dict(self, with_models=True):
        """Returns dict representation of model.

        :param with_models: Adds information about nested models to the dict.
        :type with_models: bool
        :rtype: dict
        """
        ret = dict()

        for key, value in self.get_data(with_models).items():
            ret[key] = value if not isinstance(value, IModel) else value.to_dict(with_models)

        return ret

    def __setattr__(self, key, value):
        """Sets models attribute.

        :param key: Attribute name.
        :type key: str
        :param value: Attribute value.
        :type value: str|dict|list
        :rtype: None
        """
        if key[0] != '_':
            if not getattr(self, key) is None and issubclass(getattr(self.__class__, key), IModel):
                super().__setattr__(key, getattr(self.__class__, key)(value, self.is_new()))
                if key in self.__data:
                    self.__data.pop(key)
            else:
                self.__data[key] = value
        else:
            super().__setattr__(key, value)

    def __getattr__(self, key):
        """Returns attributes value if key exists and None otherwise.

        :param key: Attribute name.
        :type key: str
        :rtype: str|list|dict
        """
        if key in self.__data:
            return self.__data[key]
        return None


class AModelAdapter(IModelAdapter):
    """Provides interfaces to work with adapter."""

    __read_adapter__ = None
    "Models read adapter name."

    __write_adapter__ = None
    "Models write adapter name."

    @classmethod
    def get_read_adapter(cls):
        """Returns models read adapter name.

        :rtype: str
        """
        return cls.__read_adapter__

    @classmethod
    def get_write_adapter(cls):
        """Returns models write adapter name.

        :rtype: str
        """
        return cls.__write_adapter__

    @classmethod
    def __get_read_adapter_inst(cls):
        """Returns read adapter instance.

        :rtype: IAdapter
        """
        return PyAR.get_adapter(cls.get_read_adapter())

    @classmethod
    def __get_write_adapter_inst(cls):
        """Returns write adapter instance.

        :rtype: IAdapter
        """
        return PyAR.get_adapter(cls.get_write_adapter())

    @classmethod
    def find(cls, **kwargs):
        """Find entities and returns it as list of models.

        :rtype: list
        """
        return cls.__get_read_adapter_inst().read(cls, **kwargs)

    @classmethod
    def find_one(cls, **kwargs):
        """Returns firs element of found entities.

        :rtype: IModel|None
        """
        result = cls.find(**kwargs)
        return result[0] if len(result) else None

    def create(self, **kwargs):
        """Creates model.

        :rtype: bool
        """
        return self.__get_write_adapter_inst().create(self, **kwargs)

    def update(self, **kwargs):
        """Updates model.

        :rtype: bool
        """
        return self.__get_write_adapter_inst().update(self, **kwargs)

    def delete(self, **kwargs):
        """Deletes model.

        :rtype: bool
        """
        return self.__get_write_adapter_inst().delete(self, **kwargs)

    def save(self, **kwargs):
        """Saves model.

        :rtype: bool
        """
        if self.is_new():
            return self.create(**kwargs)
        else:
            return self.update(**kwargs)


class AModel(IModel, AModelData, AModelAdapter):
    """PyAR model abstract class."""

    __resource__ = None
    "Models resource name."

    def __init__(self, data=None, is_new=True):
        """Constructor.
        Sets models data.

        :param data: Models data.
        :type data: dict
        """
        self.__is_new = True
        self.set_is_new(is_new)
        super().__init__(data)

    def is_new(self):
        """Returns whether this model is new.

        :rtype: bool
        """
        return self.__is_new

    def set_is_new(self, value):
        """Sets is new state for model.

        :param value: Value of state.
        :type value: bool
        :rtype: None
        """
        self.__is_new = bool(value)

    @classmethod
    def get_resource(cls):
        """Returns models resource name.

        :rtype: str
        """
        if cls.__resource__ is None:
            return '_'.join([item.lower() for item in re.findall('[A-Z][a-z]*', cls.__name__)])

        return cls.__resource__

