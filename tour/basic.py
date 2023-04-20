from datetime import datetime, date, timedelta
day_list = []

# X append 는 한 개만 가능!
# day_list.append('2020-01-01', '2020-01-02', '2020-01-04')
# Q 웹 폼에서 날짜를 받아서, date 객체로.
form_day = '2013-1-2'
# - 파이썬에서 날짜 연산을 위해, date() 의 매개변수 형식으로 parsing해서 변수에 담기:
# strptime(문자열, 포맷) : datetime 객체로 변환
parsed_day = datetime.strptime(form_day, "%Y-%m-%d")

print("폼->datetime객체 : ", parsed_day)
# print("datetime.strftime : ", strf_day)
for item in range(10):
    day = parsed_day+timedelta(days=item)
    day = day.strftime('%Y-%m-%d')
    day_list.append(day)

print(day_list)
# tour 객체에 {'day_list':[,,,,]}로 저장   
tour = {}
tour['day_list'] = day_list
tour['d_city'] = '인천'
# print(tour)
tour['r_city'] = '다낭'
# print(tour)
# print(tour['r_date'])
print('dict_items객체 반환 :',tour.items())
# tour 객체중, 
for k, v in tour.items():
    # print(k, v)
    for item in v:
        print(item)