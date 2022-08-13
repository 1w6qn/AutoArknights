class ItemGet:
    def __init__(self,data):
        self.__dict__.update(data)
class CharGet:
    def __init__(self,data):
        self.__dict__.update(data)
        if 'itemGet' in data:
            ItemGet(data['itemGet'])