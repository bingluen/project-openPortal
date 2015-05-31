# coding=UTF-8
from __future__ import print_function
import requests
from bs4 import BeautifulSoup
import re
import codecs

proxy = {
	"http": "http://proxy.hinet.net:80",
	"https": "https://proxy.hinet.net:80"
}

class CourseCatcher:
	def __init__(self):
		self.url = 'https://portal.yzu.edu.tw/cosSelect/Index.aspx'
		self.requests = requests.Session();
		self.database = codecs.open("database.sql", "w", "utf-8")
		self.database.write(u'\ufeff')
		self.database.write(u'INSERT INTO `coursedatabase` (`id`, `code`, `class`, `department`, `degree`, `credit`, `chinese_name`, `chinese_teacherName`, `type`, `url`, `year`, `semester`, `time`) VALUES\r\n')
		self.eco_viewstate = '';
		self.eco_eventvalidation = '';
		self.eco_viewstategenerator = '';
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

	def __del__(self):
		self.database.close()

	def catch(self, catchYear, catchSemester, department, degree):
		## 第一次連線 - 抓環境變數
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
					courseData['time'] = rowData[5].text.replace('        ', ',')

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

			newCourselist.append(course)

		return newCourselist
	
	def writeRow(self, courseList):
		"""
		(`id`, `code`, `class`, 
			`department`, `degree`, `credit`, 
			`chinese_name`, `chinese_teacherName`, `type`, 
			`url`, `year`, `semester`, 
			`time`)
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

	def execute(self):
		for department in self.legalDepartment:
			for degree in range(1,5):
				print('catch department = ' + str(department) + ' degree = ' + str(degree), end='')
				parserList = self.parserList(self.catch(104, 1, department, degree), 104, 1, department, degree)
				if parserList is not None:
					self.writeRow(self.parseCourse(parserList))
					print('.........Finish')
				else:
					print('.........Empty')


		

courseCatcher = CourseCatcher()
courseCatcher.execute()