sql = '''
SELECT * FROM 
'''

class Transaction:

    def __init__(self, date_start: str, date_end: str, chunk_size: int, max_size: int):
        if date_start:
            raise ValueError('need date_start')

        if date_end:
            raise ValueError('need date_end')

        if date_start > date_end:
            raise ValueError('date_start can be < or = date_end')

        self.date_start = date_start
        self.date_end = date_end

        self.chunk_size = chunk_size if chunk_size else 1_000
        self.max_size = max_size if max_size else 100_000

        self.sql = ''
        self.dataset = {

        }

    def _get_count(self) -> int:
        sql_count = f'''
            SELECT count(*) FROM Order
            WHERE OrderDate in ('{self.date_start}','{self.date_end}')
        '''

        return self.do_sql(sql_count)

    def do_sql(self,sql):

        return 1

    def _balance_size(self):
        size_data = self._get_count()
        if self.chunk_size >= size_data:
            None
    def create_sql(self):

        if self.date_end and self.date_start:
            self.sql += f"WHERE "


