s = set()

s.add(1)
s.add(1)
s.add(2)
s.add(2)
s.add(2)

# s > {1, 2}

s.clear()
# s > {}

s = {1,2,3,4}
s.discard(2)
# Remove element = 2

s = {1,2,3}
sc = s.copy()
# Copy set s to set sc, 2 separated sets
sc.add(4)
s.difference(sc)
# Return difference elements: what in s, not in sc
s.difference_update(sc)
# Assign difference elements to s

s1 = {1,2,3}
s2 = {1,3,4}
s1.intersection(s2)
# Return set of same element
s1.intersection_update(s2)
# assign set of same element to s1

s1 = {1,2,3}
s2 = {1,3,4}
s3 = {5}

s1.isdisjoint(s2)
# Bool, True if no same elements, False if have
s1.isdisjoint(s3)

s1.issubset(s2)
# Bool, subset

s1.isupperset(s2)
# Bool, if s1 contains s2

s1.symmetric_difference(s2)
# ~ s2.symmetric_difference(s1), what is in s1, not in s2 and in s2, not in s1
# {1,2,3} {1,4,5} > {2,3,4,5}

s1.union(s2)
# what in s1, in s2 > 1,2,3,4,5

s1.update(s2)
# add what in s2 to s1