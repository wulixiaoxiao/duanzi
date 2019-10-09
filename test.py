import json


f = open('jstr.txt', 'r', encoding='utf-8')
jstr = f.read()
data = json.loads(jstr)
print(data)