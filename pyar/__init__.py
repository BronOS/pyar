"""
    Main PyAR package.
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

from .base import PyAR

from .adapter import IAdapter, AAdapter, AAdapterConfig

from .model import AModel, AModelAdapter, AModelData, IModel, IModelData, IModelNew, IModelAdapter, ModelMetaRegister

from .sql_model import Relation, ASQLModel, ASQLModelFinder, ASQLModelLastData, ASQLModelPK, BelongToRelation, \
    HasManyRelation, HasOneRelation

from .exception import AdapterConfigKeyException, AdapterExecuteException, AdapterNotExistsException, \
    AdapterTypeException, ModelFieldNameException, ModelTypeException, PyARException, ModelNotExistsException, \
    RelationFieldNotExistsException, SQLAdapterExecuteException, SQLModelPartNotExistsException

from .adapters.jira import JiraReaderAdapter
from .adapters.mysql import MySQLAdapter