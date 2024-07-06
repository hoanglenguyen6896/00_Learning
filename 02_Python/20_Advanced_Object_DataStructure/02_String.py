s = 'hello world'
cap_first = s.capitalize()  # Capitalize first char

s.lower()
s.upper()

s.count('o')                # Count number of 'o'
s.find('o')                 # Find first index of 'o'
s.center(20, 'z')           # 'zzzzhello worldzzzzz'

s.isalnum()                 # Bool check alphanumeric (abc123...)
s.isalpha()                 # Bool check alphabet (abc)
s.islower()                 # Bool all is lower
s.isupper()
s.isspace()                 # Bool contains space
s.istitle()                 # Bool is title (all first char of a word is upper)
print("Hello, This No.".istitle()) # True
s.endswith('o')             # Bool end with 'o'

s.split('e')                # split to list at char 'e', give "" as a element if str have sth like 'ee'
# 'heheehhheheheheeeeehhehhehe'.split('e')
# >> ['h', 'h', '', 'hhh', 'h', 'h', 'h', '', '', '', '', 'hh', 'hh', 'h', '']