typeData = {
    'list',
    'dict',
    'set'
    'sql'
}


class Preprocessing:
    def __init__(self, data, type):
        self.data = data
        if type in typeData:
            self.type = type
        else:
            raise ValueError(f"type - {type} not support")

    def convert(self):
        convertFunc = {
            'list': self.__convert_list(),
            'sql': self.__convert_sql()
        }
        return convertFunc[self.type]

    def __convert_sql(self):
        helper = {}
        for tr in self.data:
            if tr[2] in helper:
                helper[tr[2]].add(tr[0])
            else:
                helper[tr[2]] = set(tr[0])

        transactions = []
        for (_, v) in helper.items():
            transactions.append(set(v))

    def __convert_list(self):
        return [set(i) for i in self.data]

    def __convert_dict(self):
        pass

    def convert_set(self):
        pass
