from datetime import datetime, date, timedelta
day_list = []

# X append 는 한 개만 가능!
# day_list.append('2020-01-01', '2020-01-02', '2020-01-04')
# Q 웹 폼에서 날짜를 받아서, date 객체로.
form_day = '2013-1-2'
parsed_day = datetime.strptime(form_day, "%Y-%m-%d")

for item in range(10):
    day = parsed_day+timedelta(days=item)
    day = day.strftime('%Y-%m-%d')
    day_list.append(day)

print(f'리스트: {day_list}')
# //TODO: 리스트를 객체에 저장
tour = {}
# tour['day_list'] = day_list
tour['day_list'] = day_list
print(day_list)
tour['d_city'] = '인천'
# print(tour)
tour['r_city'] = '다낭'
# print(tour)
# print(tour['r_date'])


# tour 객체중, 
# tour.keys(), values(), items()
for k, v in tour.items():
    print(f'{k}:{v}')
    for item in v:
        print(item)