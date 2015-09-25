# coding=UTF-8
from __future__ import print_function
import requests
from bs4 import BeautifulSoup
import re
import codecs
import json
from datetime import datetime


proxy = {
}

class CourseCatcher:
	def __init__(self):
		self.url = 'https://portal.yzu.edu.tw/cosSelect/Index.aspx'
		self.requests = requests.Session()
		self.courseData = {
			'update' : str(datetime.now()) ,
			'course': [],
			'courseCount': 0,
			'department': [
				{'departmentCode' : '300', 'departmentName': '工程學院'},
				{'departmentCode' : '302', 'departmentName': '機械工程學系學士班'},
				{'departmentCode' : '303', 'departmentName': '化學工程與材料科學學系學士班'},
				{'departmentCode' : '305', 'departmentName': '工業工程與管理學系學士班'},
				{'departmentCode' : '322', 'departmentName': '機械工程學系碩士班'},
				{'departmentCode' : '323', 'departmentName': '化學工程與材料科學學系碩士班'},
				{'departmentCode' : '325', 'departmentName': '工業工程與管理學系碩士班'},
				{'departmentCode' : '329', 'departmentName': '生物科技與工程研究所碩士班'},
				{'departmentCode' : '330', 'departmentName': '先進能源碩士學位學程'},
				{'departmentCode' : '352', 'departmentName': '機械工程學系博士班'},
				{'departmentCode' : '353', 'departmentName': '化學工程與材料科學學系博士班'},
				{'departmentCode' : '355', 'departmentName': '工業工程與管理學系博士班'},
				{'departmentCode' : '500', 'departmentName': '管理學院'},
				{'departmentCode' : '505', 'departmentName': '管理學院學士班'},
				{'departmentCode' : '530', 'departmentName': '管理學院經營管理碩士班'},
				{'departmentCode' : '531', 'departmentName': '管理學院財務金融暨會計碩士班'},
				{'departmentCode' : '532', 'departmentName': '管理學院管理碩士在職專班'},
				{'departmentCode' : '554', 'departmentName': '管理學院博士班'},
				{'departmentCode' : '600', 'departmentName': '人文社會學院'},
				{'departmentCode' : '601', 'departmentName': '應用外語學系學士班'},
				{'departmentCode' : '602', 'departmentName': '中國語文學系學士班'},
				{'departmentCode' : '603', 'departmentName': '藝術與設計學系學士班'},
				{'departmentCode' : '604', 'departmentName': '社會暨政策科學學系學士班'},
				{'departmentCode' : '621', 'departmentName': '應用外語學系碩士班'},
				{'departmentCode' : '622', 'departmentName': '中國語文學系碩士班'},
				{'departmentCode' : '623', 'departmentName': '藝術與設計學系(藝術管理碩士班)'},
				{'departmentCode' : '624', 'departmentName': '社會暨政策科學學系碩士班'},
				{'departmentCode' : '656', 'departmentName': '文化產業與文化政策博士學位學程'},
				{'departmentCode' : '700', 'departmentName': '資訊學院'},
				{'departmentCode' : '304', 'departmentName': '資訊工程學系學士班'},
				{'departmentCode' : '701', 'departmentName': '資訊管理學系學士班'},
				{'departmentCode' : '702', 'departmentName': '資訊傳播學系學士班'},
				{'departmentCode' : '721', 'departmentName': '資訊管理學系碩士班'},
				{'departmentCode' : '722', 'departmentName': '資訊傳播學系碩士班'},
				{'departmentCode' : '723', 'departmentName': '資訊社會學碩士學位學程'},
				{'departmentCode' : '724', 'departmentName': '資訊工程學系碩士班'},
				{'departmentCode' : '725', 'departmentName': '生物與醫學資訊碩士學位學程'},
				{'departmentCode' : '751', 'departmentName': '資訊管理學系博士班'},
				{'departmentCode' : '754', 'departmentName': '資訊工程學系博士班'},
				{'departmentCode' : '800', 'departmentName': '電機通訊學院'},
				{'departmentCode' : '301', 'departmentName': '電機工程學系學士班'},
				{'departmentCode' : '307', 'departmentName': '通訊工程學系學士班'},
				{'departmentCode' : '308', 'departmentName': '光電工程學系學士班'},
				{'departmentCode' : '326', 'departmentName': '電機工程學系碩士班'},
				{'departmentCode' : '327', 'departmentName': '通訊工程學系碩士班'},
				{'departmentCode' : '328', 'departmentName': '光電工程學系碩士班'},
				{'departmentCode' : '356', 'departmentName': '電機工程學系博士班'},
				{'departmentCode' : '357', 'departmentName': '通訊工程學系博士班'},
				{'departmentCode' : '358', 'departmentName': '光電工程學系博士班'},
				{'departmentCode' : '901', 'departmentName': '通識教學部'},
				{'departmentCode' : '903', 'departmentName': '軍訓室'},
				{'departmentCode' : '904', 'departmentName': '體育室'},
				{'departmentCode' : '906', 'departmentName': '國際語言文化中心'},
				{'departmentCode' : '907', 'departmentName': '國際兩岸事務室'}
			]
		}
		##self.database = codecs.open("database.sql", "w", "utf-8")
		##self.database.write(u'\ufeff')
		##self.database.write(u'INSERT INTO `coursedatabase` (`code`, `class`, `department`, `degree`, `credit`, `chinese_name`, `chinese_teacherName`, `type`, `url`, `year`, `semester`, `time`) VALUES\r\n')
		self.jsonDB = codecs.open("database.json", "w", "utf-8")
		##self.jsonDB = write(u'\ufeff')
		self.eco_viewstate = ''
		self.eco_eventvalidation = ''
		self.eco_viewstategenerator = ''
		self.legalDepartment = [300, 302, 303, 305, 322,
			323, 325, 329, 330, 352,
			353, 355, 500, 505, 530,
			531, 532, 554, 600,
			601, 602, 603, 604, 621,
			622, 623, 624, 700, 304,
			701, 702, 721, 722, 723,
			724, 725, 751, 754, 800,
			301, 307, 308, 326, 327,
			328, 356, 357, 358, 901,
			903, 904, 906, 907];
		self.testDepartment = [300, 302];

	###def __del__(self):
		##self.database.close()

	def catch(self, catchYear, catchSemester, department, degree):
		## 第一次連線 - 抓環境變數ß
		try:
			content = self.requests.get(self.url, proxies=proxy).text
		except requests.exceptions.ConnectionError:
			print ('Department ' + str(department))

		self.eco_viewstate = re.findall('id="__VIEWSTATE" value="([^\r\n]*)" />', content, re.S)[0]
		self.eco_eventvalidation = re.findall('id="__EVENTVALIDATION" value="([^\r\n]*)" ', content, re.S)[0]
		self.eco_viewstategenerator = re.findall('id="__VIEWSTATEGENERATOR" value="([^\r\n]*)" ', content, re.S)[0]

		## 第二次連線

		self.postData = {
			'__VIEWSTATE': self.eco_viewstate.decode('utf-8'),
			'__VIEWSTATEGENERATOR': self.eco_viewstategenerator.decode('utf-8'),
			'__EVENTVALIDATION': self.eco_eventvalidation.decode('utf-8'),
	        'DDL_YM': str(catchYear)+','+str(catchSemester)+'  ',
	        'DDL_Dept': department,
	        'DDL_Degree': '0',
	        'Q': 'RadioButton1',
	        '__EVENTTARGET': 'DDL_Dept',
	        '__EVENTARGUMENT': '',
	        '__LASTFOCUS': '',
	        'Button1': '\xe7\x99\xbb\xe5\x85\xa5'
		}

		try:
			content = self.requests.post(self.url, data=self.postData, proxies=proxy).text
		except requests.exceptions.ConnectionError:
			print ('Department ' + str(department))

		## 第三次連線
		self.eco_viewstate = re.findall('id="__VIEWSTATE" value="([^\r\n]*)" />', content, re.S)[0]
		self.eco_eventvalidation = re.findall('id="__EVENTVALIDATION" value="([^\r\n]*)" ', content, re.S)[0]
		self.eco_viewstategenerator = re.findall('id="__VIEWSTATEGENERATOR" value="([^\r\n]*)" ', content, re.S)[0]
		self.postData = {
			'__VIEWSTATE': self.eco_viewstate.decode('utf-8'),
			'__VIEWSTATEGENERATOR': self.eco_viewstategenerator.decode('utf-8'),
			'__EVENTVALIDATION': self.eco_eventvalidation.decode('utf-8'),
	        'DDL_YM': str(catchYear)+','+str(catchSemester)+'  ',
	        'DDL_Dept': department,
	        'DDL_Degree': degree,
	        'Q': 'RadioButton1',
	        '__EVENTTARGET': '',
	        '__EVENTARGUMENT': '',
	        '__LASTFOCUS': '',
	        'Button1': '\xe7\x99\xbb\xe5\x85\xa5'
		}

		try:
			content = self.requests.post(self.url, data=self.postData).text
		except requests.exceptions.ConnectionError:
			print ('Department ' + str(department))

		return content

	def parserList(self, content, year, semester, department, degree):
		dom = BeautifulSoup(content, 'lxml')
		courseList = []

		if dom.find('table', id='Table1').find('td', title='No course was selected') is not None:
			return None

		for row in dom.find('table', id='Table1').find_all('tr'):
			try:
				if row['class'][0] == u'title_line':
					continue
				rowData = row.find_all('td')
				courseData = {}
				if len(rowData) > 1:

					#Detail URL
					courseData['url'] = 'https://portal.yzu.edu.tw/cosSelect/'+rowData[1].a['href']

					#english & chinese name of course
					courseName = rowData[3].find_all('a')
					courseData['chinese_name'] = courseName[0].text

					#type
					courseData['type'] = rowData[4].text

					#class time
					courseData['time'] = ', '.join(re.findall('([0-9]{3}) ', rowData[5].text, re.S))

					#classroom
					classroomPairString = re.sub('<[/]?span>', '', str(rowData[5].find('span'))).replace('<br/>', '\n').replace(' ', '')
					classroomPair = {}
					try:
						for i in classroomPairString.split('\n'):
							stringSplit = i.split(',')
							classroomPair[stringSplit[0]] = stringSplit[1]
						courseData['classroom'] = classroomPair
					except IndexError as e:
						print(courseData['chinese_name'])
						print(e)
						print(classroomPairString)
						print(stringSplit)
						courseData['classroom'] = ''

					#teacher name
					courseData['teacher'] = re.findall('[^()]*', rowData[6].text, re.S)[0]

					#year
					courseData['year'] = year

					#semester
					courseData['semester'] = semester

					#department
					courseData['department'] = department

					#degree
					courseData['degree'] = degree


					courseList.append(courseData)
			except KeyError as e:
				print (e)
				continue

		return courseList

	def parseCourse(self, courseList):
		newCourselist = []
		for course in courseList:
			try:
				content = self.requests.get(course['url'], proxies=proxy).text
			except requests.exceptions.ConnectionError:
				print ('ConnectionError - Url ' + course['url'])

			dom = BeautifulSoup(content, 'lxml')

			data = dom.find('div', id='Cos_info').table.find_all('tr')[1].find_all('td')

			#code
			course['code'] = data[2].text.replace(' ', '')

			#class
			course['class'] = data[3].text

			#credit
			course['credit'] = int(data[4].text)

			#create uid
			course['uid'] = self.courseData['courseCount'] + 1

			newCourselist.append(course)

			self.courseData['courseCount'] =  self.courseData['courseCount'] + 1

		return newCourselist

	def writeRow(self, courseList):
		"""
		(`id`, `code`, `class`,
			`department`, `degree`, `credit`,
			`chinese_name`, `chinese_teacherName`, `type`,
			`url`, `year`, `semester`,
			`time`)
		"""
		###print (json.dumps(courseList))
		"""
		for row in courseList:
			self.database.write(u'(')
			self.database.write(u'\''+row['code']+u'\', ')
			self.database.write(u'\''+row['class']+u'\', ')
			self.database.write(u'\''+str(row['department'])+u'\', ')
			self.database.write(u'\''+str(row['degree'])+u'\', ')
			self.database.write(u'\''+str(row['credit'])+u'\', ')
			self.database.write(u'\''+row['chinese_name']+u'\', ')
			self.database.write(u'\''+row['teacher']+u'\', ')
			self.database.write(u'\''+row['type']+u'\', ')
			self.database.write(u'\''+row['url']+u'\', ')
			self.database.write(u'\''+str(row['year'])+u'\', ')
			self.database.write(u'\''+str(row['semester'])+u'\', ')
			self.database.write(u'\''+row['time']+u'\'')
			self.database.write(u'), \r\n')
		"""

	def execute(self):
		for department in self.legalDepartment:
			for degree in range(1,5):
				print('catch department = ' + str(department) + ' degree = ' + str(degree), end='')
				parserList = self.parserList(self.catch(104, 1, department, degree), 104, 1, department, degree)
				if parserList is not None:
					self.courseData['course'] = self.courseData['course'] + self.parseCourse(parserList)
					print('.........Finish')
				else:
					print('.........Empty')
		json.dump(json.dumps(self.courseData), self.jsonDB)




courseCatcher = CourseCatcher()
courseCatcher.execute()
