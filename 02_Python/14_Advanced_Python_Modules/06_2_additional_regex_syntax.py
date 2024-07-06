import re

print(re.search(r'cat', 'The cat is here'))

print(re.search(r'cat dog ascasc', 'The cat is here'))

print(re.search(r'cat|dog|ascasc', 'The cat is here'))

print(re.findall(r'.at', 'The cat in the hat sat that'))

# Contain ---at, return with 3 char with at
print(re.findall(r'...at', 'The cat in the hat sat that'))

# string start with number: ^()
print(re.findall(r'^\d','1 is a number 2'))
print(re.findall(r'^\d','The 1 is a number 2'))

# string end with number: ()$
print(re.findall(r'\d$','The 1 is a number'))
print(re.findall(r'\d$','The 1 is a number 2'))

# exclude and split every letter
pattern = r'[^\d]'

print(re.findall(pattern,'The 1 is a number 2 in this example'))

# exclude and split in to word by number
pattern = r'[^\d]+'

print(re.findall(pattern,'The 1 is a number 2 in this example'))

# Remove punctuation, split into word
# can use ' 'join(example) to join word of a list with space
print(re.findall(r'[^!.? ]+', "Hello. This is !, and here is ?"))
print(re.findall(r'[^!.?]+', "Hello. This is !, and here is ?"))
example = re.findall(r'[^!.? ]+', "Hello. This is !, and here is ?")
print(' '.join(example))

text = 'Haha you do-something and make no-mistake'
pattern = r'[\w]+-[\w]+'
print(re.findall(pattern, text))

text_1 = 'Today newspaper on the table'
text_2 = 'You have netflix?'
text_3 = 'Have never you gone to school'

pattern = r'ne(wspaper|tflix|ver)'
print(re.search(pattern, text_1))
print(re.search(pattern, text_2))
print(re.search(pattern, text_3))