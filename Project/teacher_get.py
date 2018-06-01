# -*- coding: utf-8 -*-
rooms = {}
import requests 
import json	
from bs4 import BeautifulSoup

s = requests.Session()

s.get("http://intranet2.kbtu.kz/login.aspx")

data = {
	"uname": "n_egemberdi",
	"pwd": "Kbtu2017"
}
s.post("http://intranet2.kbtu.kz/login.aspx", data = data)

r = s.get("http://intranet2.kbtu.kz/OR2/OR.Public/")
html = BeautifulSoup(r.text, "html.parser")

options = html.select("#_ctl0__ctl0_ddlRooms option")

for option in options:
	if option['value'] != -1:
		rooms[option.text] = int(option['value'])

def get_data(get_rooms):

	import requests 
	import json	
	from bs4 import BeautifulSoup
	
	s = requests.Session()
	
	s.get("http://intranet2.kbtu.kz/login.aspx")
	
	data = {
		"uname": "n_egemberdi",
		"pwd": "Kbtu2017"
	}
	s.post("http://intranet2.kbtu.kz/login.aspx", data = data)

	r = s.get("http://intranet2.kbtu.kz/OR2/OR.Public/")
	html = BeautifulSoup(r.text, "html.parser")
	
	options = html.select("#_ctl0__ctl0_ddlRooms option")

	__VIEWSTATE = html.select("input[name=__VIEWSTATE]")[0]['value']
	get_rooms = str(get_rooms)
	data = {			
				"__VIEWSTATE": __VIEWSTATE,
				"_ctl0:_ctl0:ddlFaculties": "00000000-0000-0000-0000-000000000000",
				"_ctl0:_ctl0:ddlSpecialities": "00000000-0000-0000-0000-000000000000",
				"_ctl0:_ctl0:selCourses": -1,
				"_ctl0:_ctl0:ddlRooms": get_rooms,
				"_ctl0:_ctl0:btnShowSchedule": "Показать"
			}
	r = s.post("http://intranet2.kbtu.kz/OR2/OR.Public/Default.aspx", data = data)
	
	html = BeautifulSoup(r.text, "html.parser")
	trs = html.select("#_ctl0__ctl0_Schedule1 table tr")
	schedule = {}

	for day in range(1, 8):
		schedule[day] = {}	
		for hour in range(8, 23):
			schedule[day][hour] = []
	h = 8
	wd = 1
	for tr in trs[2::2]:
		if h > 22:
			h = 8
		iterr = -1
		tds = tr.select('td')
		for td in tds:
			iterr += 1
			if wd > 7:
				wd = 1
			text = "".join([str(x) for x in td.contents])
			span = td.select("span span")[0]
			if span["id"]:
				text = text.replace("<span>", "").replace('<span id="'+ span["id"]+ '">', "").replace("</span>", "").replace("</br>", "")
			lines = text.split("<br>")
			for line in lines:
				inline = line.strip().replace("\n", "").replace("\t", "").replace("\r", "")
				
				if len(inline) == 0:
					continue
				# print(inline)
				# print("======")
				schedule[wd][h].append(inline)
				# course, teacher, room 
				#schedule[wd][h].append((course, teacher, room))
			if h > 18 and iterr % 2 == 0:
				continue
			wd += 1
		h += 1

	teachers = {}
	def get_name(text):
		lesson = ''
		name = ''
		lesson_type=''
		terra = str(text)[2:].split()
		
		lesson_type = ' '.join(terra[-3:-2])
		name = ' '.join(terra[-5:-3])
		lesson = ' '.join(terra[0:-5])
		return name, lesson, lesson_type

#	name:{lesson:{room:['fri 15:00 p', 'mon 15:00 p']}}


	file = open('teacher_json.json', encoding = 'utf-8')
	teachers = json.loads(file.read())
	file.close()
	days = ['XXX', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
	for day in range(1, 8):
		for hour in range(8, 23):
			room = get_rooms
			name_of_teacher, lesson_in_room, lesson_type = get_name(schedule[day][hour])
			
			if name_of_teacher not in teachers:
				teachers[name_of_teacher] = {}
				teachers[name_of_teacher][room] = {}
				teachers[name_of_teacher][room][lesson_in_room] = []
				teachers[name_of_teacher][room][lesson_in_room].append(days[day] + ' ' + str(hour) + ':' + '00 ' + lesson_type)
			
			if room not in teachers[name_of_teacher]:
				teachers[name_of_teacher][room] = {}
				teachers[name_of_teacher][room][lesson_in_room] = []
				teachers[name_of_teacher][room][lesson_in_room].append(days[day] + ' ' + str(hour) + ':' + '00 ' + lesson_type)
			
			if lesson_in_room not in teachers[name_of_teacher][room] :
				teachers[name_of_teacher][room][lesson_in_room] = []
				teachers[name_of_teacher][room][lesson_in_room].append(days[day] + ' ' + str(hour) + ':' + '00 ' + lesson_type)
			
			if str(days[day] + ' ' + str(hour) + ':' + '00 ' + lesson_type) not in teachers[name_of_teacher][room][lesson_in_room]:
				teachers[name_of_teacher][room][lesson_in_room].append(days[day] + ' ' + str(hour) + ':' + '00 ' + lesson_type)
			

	teachers[''] = {'EMPTY':'ROOms'}
	file = open('teacher_json.json','w')
	file.write(json.dumps(teachers))
	file.close()
	return teachers

data1 = get_data(1)
for i in rooms:
	get_data(i)
	print(i)

#print(data1['Есмуханов Даурен']['367'] )
# {
# 'Programming technologies(1-курс)': 
# 	['Mon 10:00 П', 
# 	'Mon 11:00 П', 
# 	'Tue 15:00 П', 
# 	'Tue 16:00 П', 
# 	'Wed 10:00 ЛБ', 
# 	'Wed 11:00 ЛБ', 
# 	'Fri 13:00 ЛБ', 
# 	'Fri 14:00 ЛБ']
# }
