from DB.DBase import Postgres
import pandas as pd

meta = {
    'host': 'localhost',
    'port': '5432',
    'user': 'avito',
    'password': '0000',
    'db': 'avitodb'
}

type = {
    'csv': pd.read_csv
}


def get_dataset(path: str, format: str, meta):
    if format in type:
        dataset = type[format](path, **meta)
        return dataset
    else:
        raise ValueError('format not supported')


class Transaction:

    def __init__(self, date_start: str, date_end: str, chunk_size: int = 1_000, max_size: int = 100_000):
        if not date_start:
            raise ValueError('need date_start')

        if not date_end:
            raise ValueError('need date_end')

        if date_start > date_end:
            raise ValueError('date_start can be < or = date_end')

        self.date_start = date_start
        self.date_end = date_end

        self.chunk_size = chunk_size if chunk_size else 1_000
        self.max_size = max_size if max_size else 100_000

        self.dataset = self._dataset()

    def _get_count(self) -> int:
        sql_count = f'''
            SELECT count(*) FROM Order
            WHERE OrderDate in ('{self.date_start}','{self.date_end}')
        '''

        return self.do_sql(sql_count)

    def _do_sql(self, sql):
        with Postgres(**meta) as db:
            cur = db.cursor
            cur.execute(sql)
            data = cur.fetchall()
            db.close()
            return data

    def _balance_size(self):
        size_data = self._get_count()
        if self.chunk_size >= size_data:
            None

    def _get_data_from_db(self):
        sql = f'''
            SELECT p.name, op.Quantity, o.id FROM Order as o
            JOIN OrderProduct as op on op.OrderID = o.id
            JOIN Product as p on p.id = op.ProductID 
            WHERE OrderDate in ('{self.date_start}','{self.date_end}')
        '''

        data = self.do_sql(sql)

        if data:
            return data
        else:
            print('No data sir')
            return None

    def _dataset(self):
        data = self._get_data_from_db()

        return data

    def get_dataset(self):
        return self.dataset


if __name__ == '__main__':
    test = Transaction('1', '2')
    print(test._get_count())
