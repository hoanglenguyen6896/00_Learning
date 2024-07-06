import re

text = "The agent's phone number is 408-555-1234. Call soon!"

print('phone' in text)

pattern = 'phone'
nonthing = 'balcs'

flag = re.search(nonthing, text)
print(flag)

flag = re.search(pattern, text)
print(flag)
print(flag.span())
print(flag.start())
print(flag.end())


text_next = 'hello, say hello to me'
matches = re.findall('hello', text_next)
print(matches)
print(len(matches))

for match in re.finditer('hello', text_next):
    print(match)
    print(match.span())
    print(match.group())