"""
    PyAR exceptions package.
    ~~~~~~~~~~~~~~~~~~~~~~~~

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


class PyARException(Exception):
    """Base PyAR exception."""
    pass


class AdapterTypeException(PyARException):
    """PyAR adapter type exception."""
    pass


class AdapterNotExistsException(PyARException):
    """Adapter does not exists exception."""
    pass


class AdapterExecuteException(PyARException):
    """Adapter execute exception."""
    pass


class AdapterConfigKeyException(PyARException):
    """Adapters config key does not exists exception."""
    pass


class ModelTypeException(PyARException):
    """Model type exception."""
    pass


class ModelNotExistsException(PyARException):
    """Model not exists exception."""
    pass


class ModelFieldNameException(PyARException):
    """Field name of model exception."""
    pass


class SQLModelPartNotExistsException(PyARException):
    """Part doesn't exists exception."""
    pass


class RelationFieldNotExistsException(PyARException):
    """Relation field doesn't exists exception."""
    pass


class SQLAdapterExecuteException(PyARException):
    """SQL adapter execute exception."""
    pass

