class Good:
    def __init__(self,data):
        self.__dict__.update(data)
class Shop:
    def __init__(self,data):
        self.__dict__.update(data)
        self.goodList=[Good(i)for i in data['goodList']]
class TemplateShop:
    pass