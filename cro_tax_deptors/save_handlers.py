from slugify import slugify
from db_transfer import Transfer


class RedisTransfer(Transfer):

    def __init__(self, prefix, namespace, host, port, db):
        super().__init__(prefix=str(prefix), namespace=namespace, adapter_name='redis')

        self.set_env('HOST', host)
        self.set_env('PORT', port)
        self.set_env('DB', db)


class Handler:

    _connection = {}

    def __init__(self, category_data):
        self._category_data = category_data

    @property
    def connection(self):
        key = 'deptors:' + self._category_data['namespace']
        if key not in self._connection:
            self._connection[key] = self._handler_connection()

        return self._connection[key]


class RedisHandler(Handler):

    def _handler_connection(self):
        return RedisTransfer('deptors',
                             self._category_data['namespace'],
                             **self._category_data['connection'])

    def save(self, data):
        item = slugify(data[self._category_data['item']])
        with self.connection as conn:
            del conn[item]
            conn[item] = data

        return data[self._category_data['item']], data[self._category_data['dept_key']]