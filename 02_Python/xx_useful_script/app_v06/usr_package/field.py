import colorama

cols = 66
rows = 46

x_axis = []
y_axis = []
for element in range(cols + 1):
    if element < 10:
        x_axis.append(' ' + str(element))
        y_axis.append(' ' + str(element))
    else:
        x_axis.append(str(element))
        y_axis.append(str(element))

def replace(field_2d, xy_loc, name):
    global cols
    global rows
    loc = xy_loc.split('-')
    if name < 10:
        name = ' ' + str(name)
    elif name >= 100:
        name = '*' + str(name)[2]
    field_2d[rows - int(loc[1])][int(loc[0]) - 1] = str(name)

def print_field(bot_location):
    i = rows
    field_2d = [['  ' for i in range(cols)] for j in range(rows)]
    for bot in bot_location.keys():
        if bot_location[bot][1] in ['Available', 'Charging']:
            continue
        replace(field_2d, bot_location[bot][2], bot)
    field_str = ''
    print(colorama.Fore.GREEN + '\n' + ' '.join(x_axis))
    for row in field_2d:
        print(colorama.Fore.GREEN + y_axis[i] + colorama.Fore.YELLOW + '|'+ '.'.join(row) + '|')
        i -= 1