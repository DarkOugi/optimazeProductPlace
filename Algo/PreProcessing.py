
typeData = {
    'list',
    'dict',
    'set'
}



class Preprocessing:
    def __init__(self,data,type):
        self.data = data
        if type in typeData:
            self.type = type
        else:
            raise ValueError(f"type - {type} not support")
    def convert(self):
        convertFunc = {
            'list' : self.__convert_list()
        }
        return convertFunc[self.type]
    def __convert_list(self):
        return [set(i) for i in self.data]
    def __convert_dict(self):
        pass
    def convert_set(self):
        pass