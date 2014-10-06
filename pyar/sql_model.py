"""
    PyAR sql model package.
    ~~~~~~~~~~~~~~~~~~~~~~~

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


from .model import AModel
from .exception import RelationFieldNotExistsException, SQLAdapterExecuteException
from .base import PyAR


class ASQLModelLastData(AModel):
    """SQL model last data."""

    _last_query = None
    "Last query."

    _last_result = None
    "Last result/cursor."

    @classmethod
    def get_last_query(cls):
        """Returns last query.

        :rtype: str
        """
        return cls._last_query

    @classmethod
    def get_last_result(cls):
        """Returns last result/cursor.

        :rtype: Cursor
        """
        return cls._last_result


class ASQLModelPK(ASQLModelLastData):
    """SQL model primary key helper."""

    _pk_ = None
    "Models primary key."

    @classmethod
    def get_pk(cls):
        """Returns models primary key.

        :rtype: str
        """
        return cls._pk_ if cls._pk_ is not None else 'id'

    def get_id(self):
        """Returns primary's key value.

        :rtype: int
        """
        return getattr(self, self.get_pk())


class ASQLModelFinder(ASQLModelPK):
    """SQL model find helper."""

    @classmethod
    def find(cls, select=None, joins=None, where=None, having=None, limit=None, offset=None, distinct=False, group=None,
             order=None, params=dict(), **kwargs):
        """Find entities and returns it as list of models.

        :param select: Allows to specify query field. Representing the SELECT-part of the SQL statement.
        :type select: str
        :param joins: Allows to specify row sql joins. Representing the JOIN-part of the SQL statement.
        :type joins: str
        :param where: Allows to specify query conditions. Representing the WHERE-part of the SQL statement.
        :type where: str
        :param having: Allows to specify GROUP BY conditions. Representing the HAVING-part of the SQL statement.
        :type having: str
        :param limit: Allows to specify number of records. Representing the LIMIT-part of the SQL statement.
        :type limit: int
        :param offset: Allows to specify position of the beginning rows.
        Representing the OFFSET-part of the SQL statement.
        :type offset: int
        :param distinct: Allows to specify grabbing a single record per unique value in a certain field.
        Representing the DISTINCT-part of the SQL statement.
        :type distinct: bool
        :param group: Allows to specify grouping of result. Representing the "GROUP BY"-part of the SQL statement.
        :type group: str
        :param order: Allows to specify ordering of result. Representing the "ORDER BY"-part of the SQL statement.
        :type order: str
        :param params: Allows to specify query parameters.
        In other words it replaces every ":key" of builded query by value.
        :type params: dict
        :param kwargs: Allows to specify query conditions with AND statement.
        Representing the WHERE-part of the SQL statement.
        :type kwargs: dict
        :rtype: list
        """
        kwargs['select'] = select
        kwargs['joins'] = joins
        kwargs['where'] = where
        kwargs['having'] = having
        kwargs['limit'] = limit
        kwargs['offset'] = offset
        kwargs['distinct'] = distinct
        kwargs['group'] = group
        kwargs['order'] = order
        kwargs['params'] = params

        result = super().find(**kwargs)
        cls._last_query = cls.get_read_adapter_inst().get_last_query()
        cls._last_result = cls.get_read_adapter_inst().get_last_result()
        return result

    @classmethod
    def count(cls, joins=None, where=None, having=None, distinct=False, group=None,
              order=None, params=dict(), **kwargs):
        """Find entities and returns it as list of models.

        :param joins: Allows to specify row sql joins. Representing the JOIN-part of the SQL statement.
        :type joins: str
        :param where: Allows to specify query conditions. Representing the WHERE-part of the SQL statement.
        :type where: str
        :param having: Allows to specify GROUP BY conditions. Representing the HAVING-part of the SQL statement.
        :type having: str
        :param distinct: Allows to specify grabbing a single record per unique value in a certain field.
        Representing the DISTINCT-part of the SQL statement.
        :type distinct: bool
        :param group: Allows to specify grouping of result. Representing the "GROUP BY"-part of the SQL statement.
        :type group: str
        :param order: Allows to specify ordering of result. Representing the "ORDER BY"-part of the SQL statement.
        :type order: str
        :param params: Allows to specify query parameters.
        In other words it replaces every ":key" of builded query by value.
        :type params: dict
        :param kwargs: Allows to specify query conditions with AND statement.
        Representing the WHERE-part of the SQL statement.
        :type kwargs: dict
        :rtype: int
        """
        kwargs['select'] = 'COUNT(*) AS count_rows'
        kwargs['joins'] = joins
        kwargs['where'] = where
        kwargs['having'] = having
        kwargs['limit'] = 1
        kwargs['distinct'] = distinct
        kwargs['group'] = group
        kwargs['order'] = order
        kwargs['params'] = params

        model = cls.find_one(**kwargs)
        return model.count_rows if model is not None else 0

    @classmethod
    def find_one(cls, select=None, joins=None, where=None, having=None, offset=None, distinct=False, group=None,
                 order=None, params=dict(), **kwargs):
        """Find entities and returns it as list of models.

        :param select: Allows to specify query field. Representing the SELECT-part of the SQL statement.
        :type select: str
        :param joins: Allows to specify row sql joins. Representing the JOIN-part of the SQL statement.
        :type joins: str
        :param where: Allows to specify query conditions. Representing the WHERE-part of the SQL statement.
        :type where: str
        :param having: Allows to specify GROUP BY conditions. Representing the HAVING-part of the SQL statement.
        :type having: str
        :param offset: Allows to specify position of the beginning rows.
        Representing the OFFSET-part of the SQL statement.
        :type offset: int
        :param distinct: Allows to specify grabbing a single record per unique value in a certain field.
        Representing the DISTINCT-part of the SQL statement.
        :type distinct: bool
        :param group: Allows to specify grouping of result. Representing the "GROUP BY"-part of the SQL statement.
        :type group: str
        :param order: Allows to specify ordering of result. Representing the "ORDER BY"-part of the SQL statement.
        :type order: str
        :param params: Allows to specify query parameters.
        In other words it replaces every ":key" of builded query by value.
        :type params: dict
        :param kwargs: Allows to specify query conditions with AND statement.
        Representing the WHERE-part of the SQL statement.
        :type kwargs: dict
        :rtype: ASQLModel
        """
        kwargs['select'] = select
        kwargs['joins'] = joins
        kwargs['where'] = where
        kwargs['having'] = having
        kwargs['limit'] = 1
        kwargs['offset'] = offset
        kwargs['distinct'] = distinct
        kwargs['group'] = group
        kwargs['order'] = order
        kwargs['params'] = params

        result = super().find_one(**kwargs)
        cls._last_query = cls.get_read_adapter_inst().get_last_query()
        cls._last_result = cls.get_read_adapter_inst().get_last_result()
        return result

    @classmethod
    def find_by_id(cls, id):
        """Find one record by primary key.

        :param id: Value of primary key.
        :type id: int|str
        :rtype: ASQLModel
        """
        return cls.find_one(**{cls.get_pk(): id if type(id) == list else str(id)})

    @classmethod
    def find_by_query(cls, query, params=dict(), **kwargs):
        """Find one record by primary key.

        :param params: Allows to specify query parameters.
        In other words it replaces every ":key" of builded query by value.
        :type params: dict
        :param kwargs: Allows to specify query parameters as key word arguments.
        :type kwargs: dict
        :rtype: list
        """
        return cls.find(query=query, params=params, **kwargs)


class ASQLModel(ASQLModelFinder):
    """PyAR abstract sql model."""

    def get_data_models(self):
        """Returns dict of relations fields of this model.

        :rtype: dict
        """
        ret = dict()

        for key, value in self.__class__.__dict__.items():
            if isinstance(value, Relation):
                value = self.get_attr(key)
                if isinstance(value, ASQLModel):
                    ret[key] = value

        return ret

    def save(self, transactional=False, with_relations=False):
        """Saves model.

        :rtype: bool
        """
        return super().save(transactional=transactional, with_relations=with_relations)

    def create(self, transactional=True, **kwargs):
        """Creates model.

        :param transactional: Create transactional flag.
        :type transactional: bool
        :rtype: bool
        """
        last_query = []

        if transactional:
            self.get_write_adapter_inst().start_transaction()
            last_query.append(self.get_write_adapter_inst().get_last_query())

        try:
            super().create()
            self.set_is_new(False)
            setattr(self, self.get_pk(), self.get_write_adapter_inst().get_last_result().lastrowid)
            last_query.append(self.get_write_adapter_inst().get_last_query())
            self.__class__._last_result = self.get_write_adapter_inst().get_last_result()
        except SQLAdapterExecuteException as exc:
            self.__class__._last_result = self.get_write_adapter_inst().get_last_result()
            last_query.append(self.get_write_adapter_inst().get_last_query())

            if transactional:
                self.get_write_adapter_inst().rollback_transaction()
                last_query.append(self.get_write_adapter_inst().get_last_query())

            self.__class__._last_query = '; '.join(last_query)
            raise exc

        if transactional:
            self.get_write_adapter_inst().commit_transaction()
            last_query.append(self.get_write_adapter_inst().get_last_query())

        self.__class__._last_query = '; '.join(last_query)
        return True

    def update(self, transactional=True, with_relations=False, **kwargs):
        """Updates model.

        :param transactional: Create transactional flag.
        :type transactional: bool
        :param with_relations: Update relation_model models flag.
        :rtype: bool
        """
        last_query = []

        if transactional:
            self.get_write_adapter_inst().start_transaction()
            last_query.append(self.get_write_adapter_inst().get_last_query())

        try:
            super().update()
            last_query.append(self.get_write_adapter_inst().get_last_query())
            self.__class__._last_result = self.get_write_adapter_inst().get_last_result()

            if with_relations:
                for key, relation_model in self.get_data_models().items():
                    relation_model.update(transactional=False, with_relations=True)
                    last_query.append(relation_model.get_last_query())
        except SQLAdapterExecuteException as exc:
            self.__class__._last_result = self.get_write_adapter_inst().get_last_result()
            last_query.append(self.get_write_adapter_inst().get_last_query())

            if transactional:
                self.get_write_adapter_inst().rollback_transaction()
                last_query.append(self.get_write_adapter_inst().get_last_query())

            self.__class__._last_query = '; '.join(last_query)
            raise exc

        if transactional:
            self.get_write_adapter_inst().commit_transaction()
            last_query.append(self.get_write_adapter_inst().get_last_query())

        self.__class__._last_query = '; '.join(last_query)
        return True

    def delete(self):
        """Delete model.

        :rtype: bool
        """
        super().delete()
        self.__class__._last_query = self.get_write_adapter_inst().get_last_query()
        self.get_write_adapter_inst().commit_transaction()
        self.set_is_new(True)
        self.del_attr(self.get_pk())
        return True


class Relation(property):
    """PyAR models relation class."""

    def __init__(self, model_cls, foreign_key=None, relation_key=None, through=None, through_relation_key=None,
                 select=None, joins=None, where=None, having=None, limit=None, offset=None, distinct=False, group=None,
                 order=None, params=dict(), **kwargs):
        """Sets relation config.

        :param model_cls: Foreign model.
        :type model_cls: ASQLModel|str
        :param foreign_key: Foreign field name.
        :type foreign_key: str
        :param relation_key: Relation field name.
        :type relation_key: str
        :param through: A through association sets up a one-to-one relation with another model.
        :type through: Relation
        :param through_relation_key: Through relation field name.
        :type through_relation_key: str
        :param select: Allows to specify query field. Representing the SELECT-part of the SQL statement.
        :type select: str
        :param joins: Allows to specify row sql joins. Representing the JOIN-part of the SQL statement.
        :type joins: str
        :param where: Allows to specify query conditions. Representing the WHERE-part of the SQL statement.
        :type where: str
        :param having: Allows to specify GROUP BY conditions. Representing the HAVING-part of the SQL statement.
        :type having: str
        :param limit: Allows to specify number of records. Representing the LIMIT-part of the SQL statement.
        :type limit: int
        :param offset: Allows to specify position of the beginning rows.
        Representing the OFFSET-part of the SQL statement.
        :type offset: int
        :param distinct: Allows to specify grabbing a single record per unique value in a certain field.
        Representing the DISTINCT-part of the SQL statement.
        :type distinct: bool
        :param group: Allows to specify grouping of result. Representing the "GROUP BY"-part of the SQL statement.
        :type group: str
        :param order: Allows to specify ordering of result. Representing the "ORDER BY"-part of the SQL statement.
        :type order: str
        :param params: Allows to specify query parameters.
        In other words it replaces every ":key" of builded query by value.
        :type params: dict
        :param kwargs: Allows to specify query conditions with AND statement.
        Representing the WHERE-part of the SQL statement.
        :type kwargs: dict
        """
        self.__model_cls = model_cls
        self.foreign_key = foreign_key
        self.relation_key = relation_key
        self.through_relation_key = through_relation_key
        self.through = through
        self.select = select
        self.joins = joins
        self.where = where
        self.having = having
        self.limit = limit
        self.offset = offset
        self.distinct = distinct
        self.group = group
        self.order = order
        self.params = params
        self.kwargs = kwargs

        self.__data = dict()

        super().__init__(self.__get_data)

    @property
    def model_cls(self):
        """Model class getter.

        :rtype: ASQLModel
        """
        if type(self.__model_cls) is str:
            self.__model_cls = PyAR.get_model(self.__model_cls)
        return self.__model_cls

    def _get_relation_value(self):
        """Returns relation value.

        :rtype: str
        """
        value = self.parent_model.get_attr(self.relation_key)
        if value is None:
            raise RelationFieldNotExistsException('Relation field [%s] not exists.' % self.relation_key)
        return value

    def _prepare_filters(self):
        """Prepares find filters.

        :rtype: None
        """
        relation_value = self._get_relation_value()

        if self.through is not None:
            if self.through.relation_key is None:
                self.through.relation_key = '%s_%s' % (
                    self.model_cls.get_resource(),
                    self.model_cls.get_pk()
                )

            if self.through.foreign_key is None:
                self.through.foreign_key = self.model_cls.get_pk()

            self.joins = '' if self.joins is None else self.joins + ' '

            self.joins += 'LEFT JOIN %s ON (%s.%s = %s.%s)' % (
                self.through.model_cls.get_resource(),

                self.through.model_cls.get_resource(),
                self.through.relation_key,

                self.model_cls.get_resource(),
                self.through.foreign_key,
            )

            self.where = '' if self.where is None else self.where + ' AND '

            if self.through.through_relation_key is None:
                self.through.through_relation_key = '%s_%s' % (
                    self.parent_model.get_resource(),
                    self.parent_model.get_pk()
                )

            self.where += '(%s.%s = :foreign_key)' % (
                self.through.model_cls.get_resource(),
                self.through.through_relation_key,
            )
            self.params.update({'foreign_key': relation_value})
        else:
            self.kwargs.update({self.foreign_key: relation_value})

    def __get_data(self, parent_model):
        """Loads relation data and stores it into self.__data attribute.

        :param parent_model: Relation model.
        :type parent_model: ASQLModel
        :rtype: ASQLModel|list<ASQLModel>
        """
        parent_model_hash = hash(parent_model)
        if parent_model_hash not in self.__data:
            self.parent_model = parent_model
            self.__data[parent_model_hash] = self.load()

        return self.__data[parent_model_hash]

    def load(self):
        """Loads relation data.

        :rtype: ASQLModel|list<ASQLModel>
        """
        pass


class HasManyRelation(Relation):
    """A "has many" association sets up a one-to-many relation with another model,
    such that each instance of the declaring model "has many" list of instances of the other model."""

    def load(self):
        """Loads relation data.

        :rtype: list<ASQLModel>
        """
        if self.relation_key is None:
            self.relation_key = self.parent_model.get_pk()

        if self.foreign_key is None:
            self.foreign_key = '%s_%s' % (self.parent_model.get_resource(), self.parent_model.get_pk())

        self._prepare_filters()

        return self.model_cls.find(select=self.select, distinct=self.distinct, group=self.group, joins=self.joins,
                                   limit=self.limit, offset=self.offset, order=self.order, where=self.where,
                                   params=self.params, **self.kwargs)


class HasOneRelation(Relation):
    """A "has one" association sets up a one-to-one relation with another model,
    such that each instance of the declaring model "has one" one instance of the other model."""

    def load(self):
        """Loads relation data.

        :rtype: ASQLModel
        """
        if self.relation_key is None:
            self.relation_key = self.parent_model.get_pk()

        if self.foreign_key is None:
            self.foreign_key = '%s_%s' % (self.parent_model.get_resource(), self.parent_model.get_pk())

        self._prepare_filters()

        return self.model_cls.find_one(select=self.select, distinct=self.distinct, group=self.group, joins=self.joins,
                                       limit=self.limit, offset=self.offset, order=self.order, where=self.where,
                                       params=self.params, **self.kwargs)


class BelongToRelation(Relation):
    """A "belong to" association sets up a one-to-one relation with another model,
    such that each instance of the declaring model "belongs to" one instance of the other model."""

    def load(self):
        """Loads relation data.

        :rtype: ASQLModel
        """
        if self.relation_key is None:
            self.relation_key = '%s_%s' % (self.model_cls.get_resource(), self.model_cls.get_pk())

        if self.foreign_key is None:
            self.foreign_key = self.model_cls.get_pk()

        self._prepare_filters()

        return self.model_cls.find_one(select=self.select, distinct=self.distinct, group=self.group, joins=self.joins,
                                       limit=self.limit, offset=self.offset, order=self.order, where=self.where,
                                       params=self.params, **self.kwargs)