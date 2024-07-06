"""

Character   Description         Example Pattern Code    Exammple Match
\d          A digit             file_\d\d               file_25
\w          Alphanumeric        \w-\w\w\w               A-b_1
\s          White space         a\sb\sc                 a b c
\D          A non digit         \D\D\D                  ABC
\W          Non-alphanumeric    \W\W\W\W\W              *-+=)
\S          Non-whitespace      \S\S\S\S                Yoyo

"""

# You should find Quantifiers


import re

text = '11:14:50,2134.580, 2134.580 state: P71_WAITING_TO_BEGIN -> P71_MONITOR_MOTION (delta of 0.133 sec)'\
        + '11:14:58,2142.623, Emergency begin P71_read'\
        + '11:14:58,2142.631, Emergency from  P71_read 0x02'\
        + '11:14:58,2142.650, 2142.650 state: P71_MONITOR_MOTION -> P71_MOTION_COMPLETE (delta of 8.070 sec)'\
        + '11:14:58,2142.670, Axis arrived'

phone = re.findall(r'Emergency', text)
# Method 2: phone = re.search(r'\d{3}-\d{3}-d{4}', text)
print(phone)
# print(phone.group(1))

text = 'Hello 023-123-4353'
# Use Quantifiers
phone = re.search(r'\d{3}-\d{3}-\d{4}', text)
print(phone)
print(phone.group())


# Use pattern to get a group
phone_pattern = re.compile(r'(\d{3})-(\d{3})-(\d{4})')
result = re.search(phone_pattern, text)
print(result)
print(result.group())
print(result.group(1)) # Group start at 1
print(result.group(2))
print(result.group(3))
# print(result.group(4))