import datetime
print(f"{'time':=^80}")
mytime = datetime.time(5, 30)

print(mytime)
print(mytime.minute)
print(mytime.hour)
print(mytime.second)
print(mytime.microsecond)

mytime_next = datetime.time(13,22,54,212)

print(mytime_next)
print(mytime_next.minute)
print(mytime_next.hour)
print(mytime_next.second)
print(mytime_next.microsecond)


print(f"{'datetime':=^80}")
#from datetime import datetime

my_datetime = datetime.datetime(2021, 10, 3, 14, 20, 1)
print(my_datetime)
my_datetime = my_datetime.replace(year=2020)
print(my_datetime)

my_dt1 = datetime.datetime(2021, 10, 15, 23, 15, 45)
my_dt2 = datetime.datetime(1994, 4, 5, 3, 10, 20)

print(my_dt1 - my_dt2)

print(f"{'date':=^80}")
today = datetime.date.today()
print(today)
print(today.day)
print(today.month)
print(today.year)


print(f"{'ctime':=^80}")
print(today.ctime())

print(f"{'date':=^80}")

date1 = datetime.date(2021, 11, 3)
date2 = datetime.date(2021, 1, 28)
print(date1)
print(date2)

delta_date = date1 - date2
print(delta_date)
print(delta_date.days)