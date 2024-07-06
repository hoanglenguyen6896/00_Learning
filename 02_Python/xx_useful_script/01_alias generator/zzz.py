import json

f = open('config.json', 'r')
r = json.load(f)
f.close()
print(r)