import json
class Test:
    def __init__(self, idade, name, lista):
        self.idade = idade
        self.name = name
        self.lista = lista
    def to_bytes(self):
        return json.dumps(self.__dict__, sort_keys=True).encode('utf-8')
    @staticmethod
    def from_bytes(content):
        data_dict = json.loads(content.decode('utf-8'))
        return Test(**data_dict)
    def __repr__(self):
        return 'Test(%s, %s, %s)' % (self.idade, self.name, self.lista)
    def getBy(self, id):
        return next(filter(lambda element: element['id'] == id, self.lista))
dictA = {
    "id": 1,
    "key1": "value1",
    "key2": "value2",
}
testA = Test(10, "Nome", [dictA])
bytesA = testA.to_bytes()
testB = Test.from_bytes(bytesA)
print(bytesA)
print(testB)
print(testB.to_bytes())
print(testA.getBy(1))