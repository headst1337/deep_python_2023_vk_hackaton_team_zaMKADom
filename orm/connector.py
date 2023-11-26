import aiomysql
import asyncio

AND = 'and'
OR = 'or'


class Q:

    def __init__(self, exp_type=AND, **kwargs):
        self.separator = exp_type
        self._params = kwargs

    def __str__(self):
        kv_pairs = [f'{k} = {v}' for k, v in self._params.items()]
        return f' {self.separator} '.join(kv_pairs)

    def __bool__(self):
        return bool(self._params)


class BaseExp:
    name = None

    def add(self, *args, **kwargs):
        raise NotImplementedError()

    def definition(self) -> str:
        return self.name + '\n\t' + self.line() + '\n'

    def __bool__(self):
        raise NotImplementedError()


class Select(BaseExp):

    name = 'SELECT'

    def __init__(self):
        self._params = []

    def add(self, *args, **kwargs):
        self._params.extend(args)

    def line(self) -> str:
        separator = ','
        return separator.join(self._params)

    def __bool__(self):
        return bool(self._params)


class From(BaseExp):

    name = 'FROM'

    def __init__(self):
        self._params = []

    def add(self, *args, **kwargs):
        self._params.extend(args)

    def line(self) -> str:
        separator = ','
        return separator.join(self._params)

    def __bool__(self):
        return bool(self._params)


class Where(BaseExp):

    name = 'WHERE'

    def __init__(self, exp_type=AND, **kwargs):
        self._q = Q(exp_type=exp_type, **kwargs)

    def add(self, exp_type=AND, **kwargs):
        self._q = Q(exp_type, **kwargs)
        return self._q

    def line(self):
        return str(self._q)

    def __bool__(self):
        return bool(self._q)


class Query:

    def __init__(self):
        self._data = {'select': Select(), 'from': From(), 'where': Where()}

    def SELECT(self, *args):
        self._data['select'].add(*args)
        return self

    def FROM(self, *args):
        self._data['from'].add(*args)
        return self

    def WHERE(self, *args, **kwargs):
        self._data['where'].add(*args, **kwargs)
        return self

    def INSERT_INTO(self, table_name, *columns):
        self._data['insert_into'] = {'table': table_name, 'columns': columns, 'values': []}
        return self

    def VALUES(self, *values):
        if 'insert_into' not in self._data:
            raise ValueError("INSERT_INTO must be called before VALUES.")
        self._data['insert_into']['values'].append(values)
        return self

    def CREATE(self, table_name, columns):
        create_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'`{col}` {data_type}' for col, data_type in columns.items()])})"
        return create_query

    def _lines(self):
        for key in self._data:
            if key == 'insert_into':
                insert_into = self._data[key]
                columns_str = ', '.join([f'`{col}`' for col in insert_into['columns']])
                values_str = ', '.join([f"({', '.join(['%s']*len(insert_into['columns']))})" for _ in insert_into['values']])
                yield f"INSERT INTO {insert_into['table']} ({columns_str}) VALUES {values_str};"
            elif self._data[key]:
                yield self._data[key].definition()

    def __str__(self):
        return '\n'.join(self._lines())


class AsyncMySQLConnector:
    def __init__(self, host, port, user, password, db):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.pool = None

    async def connect(self):
        self.pool = await aiomysql.create_pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db,
            loop=asyncio.get_event_loop()
        )

    async def execute(self, query, params=None):
        print(f"Executing query: {query}")
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, params)
                result = await cur.fetchall()
                await conn.commit()
        return result

    async def close(self):
        self.pool.close()
        await self.pool.wait_closed()

async def main():
    try:
        connector = AsyncMySQLConnector(host='localhost', port=8081, user='admin', password='admin', db='db')
        await connector.connect()

        create_query = (
            Query()
            .CREATE(
                table_name='USERS',
                columns={'id': 'INT AUTO_INCREMENT PRIMARY KEY', 'name': 'VARCHAR(255)', 'age': 'INT'}
            )
        )
        await connector.execute(str(create_query))

        insert_query = (
            Query()
            .INSERT_INTO('USERS', 'name', 'age')
            .VALUES('John Doe', 25)
        )
        await connector.execute(str(insert_query), insert_query._data['insert_into']['values'][0])

        select_query = (
            Query()
            .SELECT('*')
            .FROM('USERS')
        )
        result = await connector.execute(str(select_query))
        print(result)
    finally:
        await connector.close()

# Run the event loop
asyncio.run(main())
