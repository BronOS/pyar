"""
    PyAR MySQL adapter package.
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
from ..model import Model
from ..sql_model import SQLModel
from ..exception import SQLAdapterExecuteException, ModelTypeException

import pymysql
import re


class MySQLAdapter(AAdapter):
    """PyAR MySQL adapter."""

    def __init__(self, **kwargs):
        """Constructor. Sets adapter config.

        :param host: Host where the database server is located
        :param user: Username to log in as
        :param passwd: Password to use.
        :param database: Database to use, None to not use a particular one.
        :param port: MySQL port to use, default is usually OK.
        :param unix_socket: Optionally, you can use a unix socket rather than TCP/IP.
        :param charset: Charset you want to use.
        :param sql_mode: Default SQL_MODE to use.
        :param read_default_file: Specifies  my.cnf file to read these parameters from under the [client] section.
        :param conv: Decoders dictionary to use instead of the default one. This is used to provide custom marshalling of types. See converters.
        :param use_unicode: Whether or not to default to unicode strings. This option defaults to true for Py3k.
        :param client_flag: Custom flags to send to MySQL. Find potential values in constants.CLIENT.
        :param cursorclass: Custom cursor class to use.
        :param init_command: Initial SQL statement to run when connection is established.
        :param connect_timeout: Timeout before throwing an exception when connecting.
        :param ssl: A dict of arguments similar to mysql_ssl_set()'s parameters. For now the capath and cipher arguments are not supported.
        :param read_default_group: Group to read from in the configuration file.
        :param compress; Not supported
        :param named_pipe: Not supported
        :param no_delay: Disable Nagle's algorithm on the socket
        :param autocommit: Autocommit mode. None means use server default. (default: False)
        :param db: Alias for database. (for compatibility to MySQLdb)
        """
        self.__last_query = None
        self.__last_result = None
        super().__init__(**kwargs)
        self.__conn = pymysql.connect(**kwargs)

    @staticmethod
    def __check_model_type(model):
        """Checks model type.

        :param model: Methods model.
        :type model: SQLModel
        :rtype: None
        """
        if not isinstance(model, SQLModel):
            raise ModelTypeException('Model must be an instance of SQLData')

    def execute(self, query, cursor_type=None):
        """Executes query.

        :param query: Query string.
        :type query: str
        :rtype: Cursor
        """
        cursor = self.get_connection().cursor(cursor_type)
        self.__last_query = query
        self.__last_result = cursor

        try:
            cursor.execute(query)
        except pymysql.IntegrityError as exc:
            cursor.close()
            raise SQLAdapterExecuteException(exc.args)

        cursor.close()

        return cursor


    def read(self, model_cls, select=None, joins=None, where=None, having=None, limit=None, offset=None, distinct=False,
             group=None, order=None, params=dict(), query=None, **kwargs):
        """Build SQL query and execute it.

        :param model_cls: PyAR model class.
        :type model_cls: SQLModel
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
        :param query: Allows to specify full sql query.
        :type query: str
        :param kwargs: Allows to specify query conditions with AND statement.
        Representing the WHERE-part of the SQL statement.
        :type kwargs: dict
        :rtype: list
        """
        super().read(model_cls, **kwargs)

        if query is None:
            query = 'SELECT' \
                    '%s' \
                    '%s' \
                    'FROM %s' \
                    '%s' \
                    '%s' \
                    '%s' \
                    '%s' \
                    '%s' \
                    '%s' % (
                        ' DISTINCT' if distinct else '',
                        ' %s ' % select if select is not None else ' %s.* ' % model_cls.get_resource(),
                        model_cls.get_resource(),
                        ' ' + joins if joins is not None else '',
                        self.__build_read_where(where, model_cls.get_resource(), kwargs),
                        ' GROUP BY ' + group if group is not None else '',
                        ' HAVING ' + having if having is not None else '',
                        ' LIMIT ' + str(limit) if limit is not None else '',
                        ' OFFSET ' + str(offset) if offset is not None else '',
                    )

        params.update(kwargs)

        if len(params):
            params = pymysql.escape_dict(params, "'")
            pattern = re.compile('|'.join([':' + key for key in params.keys()]))
            query = pattern.sub(lambda x: params[x.group()[1:]], query)

        cursor = self.execute(query, pymysql.cursors.DictCursor)
        result = [model_cls(row, False) for row in cursor]

        return result

    @staticmethod
    def __build_read_where(where, resource, kwargs):
        """Builds SQL where part.

        :param where: Read where parameters.
        :type where: str
        :param resource: Resource name.
        :type resource: str
        :param kwargs: Read key word arguments.
        :type kwargs: dict
        :rtype: str
        """
        where_part = where if where is not None else ''

        if len(where_part) and len(kwargs):
            where_part += ' AND '

        where_part += ' AND '.join(
            ['%s.%s %s' % (
                resource,
                key,
                'IN (%s)' % ','.join([pymysql.escape_string(str(val)) for val in value]) if type(value) == list else
                '= :%s' % key
            ) for key, value in kwargs.items()]
        )

        return ' WHERE ' + where_part if len(where_part) else ''

    def get_last_query(self):
        """Returns last query.

        :rtype: str
        """
        return self.__last_query

    def get_last_result(self):
        """Returns last result.

        :rtype: Cursor
        """
        return self.__last_result

    def get_connection(self):
        """Returns connection object.

        :rtype: Connection
        """
        return self.__conn

    def __del__(self):
        """Destruct DB connection.

        :rtype: None
        """
        self.get_connection().close()

    def __get_columns(self, model):
        """Returns table columns information.

        :param model: PyAR sql model.
        :type model: SQLModel
        :rtype: dict
        """
        cursor = self.execute('SHOW COLUMNS FROM %s' % model.get_resource(False), pymysql.cursors.DictCursor)
        ret = dict((row['Field'], row) for row in cursor)
        return ret

    def __get_model_data(self, model):
        """Returns filtered model's data.

        :param model: PyAR sql model.
        :type model: SQLModel
        :rtype: dict
        """
        columns = self.__get_columns(model)
        return dict((key, value) for key, value in pymysql.escape_dict(model.get_data(False), "'").items()
                    if key in columns)

    def start_transaction(self):
        """Execute "START TRANSACTION" query.

        :rtype: None
        """
        self.execute('START TRANSACTION')

    def commit_transaction(self):
        """Execute "COMMIT" query.

        :rtype: None
        """
        self.get_connection().commit()
        self.__last_query = 'COMMIT'

    def rollback_transaction(self):
        """Execute "ROLLBACK" query.

        :rtype: None
        """
        self.get_connection().rollback()
        self.__last_query = 'ROLLBACK'

    def create(self, model):
        """Create model.

        :param model: PyAR model.
        :type model: SQLModel
        :rtype: bool
        """
        super().create(model)

        data = self.__get_model_data(model)

        if not len(data):
            raise SQLAdapterExecuteException('Nothing to insert.')

        query = 'INSERT INTO %s (%s) VALUES (%s)' % (
            model.get_resource(False),
            ','.join(data.keys()),
            ','.join(data.values()),
        )

        cursor = self.execute(query)
        return True

    def update(self, model):
        """Update model.

        :param model: PyAR model.
        :type model: SQLModel
        :rtype: bool
        """
        super().update(model)

        data = self.__get_model_data(model)

        if not len(data):
            raise SQLAdapterExecuteException('Nothing to update.')

        query = 'UPDATE %s SET %s WHERE %s = %s' % (
            model.get_resource(False),
            ', '.join(['%s = %s' % (key, value) for key, value in data.items()]),
            model.get_pk(),
            pymysql.escape_string(str(model.get_id())),
        )

        cursor = self.execute(query)
        return True

    def delete(self, model):
        """Delete model.

        :param model: PyAR model.
        :type model: SQLModel
        :rtype: bool
        """
        super().delete(model)

        query = 'DELETE FROM %s WHERE %s = %s LIMIT 1' % (
            model.get_resource(False),
            model.get_pk(),
            pymysql.escape_string(str(model.get_id())),
        )

        cursor = self.execute(query)
        return True
