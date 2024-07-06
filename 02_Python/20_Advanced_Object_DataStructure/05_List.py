l =[1,1,2,3,4,5]
l.count(0) # > 0
l.count(1) # > 2

# append(a) > a become a element, [1,2,3].appen([4,5]) > [1,2,3,[4,5]]
# extend > [1,2,3,4,5]

l.index(2) # > 2, return index of the value l.index(<value>)
# return error if not in list > try exceopt for ValueError

l.remove(1) # remove the first instance of 1, ValueError if not exist

l.reverse() # reverse

l.sort() # sort 1 > 9, a > b, must same type