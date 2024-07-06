dic = {k:v**2 for k,v in zip(['a', 'b'], range(5))}
print(dic)
# > {'a': 0, 'b': 1}
# d = {k:v**2 for k,v in zip(['a', 'b', 'c'], range(5))} > {'a': 0, 'b': 1}
# d = {k:v**2 for k,v in zip(['a', 'b'], range(100))} > {'a': 0, 'b': 1}

# Only Python 2
# d = {'k1':1, 'k2':2}
# for k in d.iteritems():
#     print(k)

# for k in d.iterkeys():
#     print(k)

# for k in d.itervalues():
#     print(k)
# d.viewitems()
# d.viewkeys()
# d.viewvalues()