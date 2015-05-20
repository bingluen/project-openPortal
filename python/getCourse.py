# coding=UTF-8
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
		self.database.write(u'INSERT INTO `coursedatabase` (`id`, `code`, `cname`, `year`, `professor`, `time`) VALUES\r\n')
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
			print 'Department ' + str(department)


		self.eco_viewstate = re.findall('id="__VIEWSTATE" value="([^\r\n]*)" />', content, re.S)[0]
		self.eco_eventvalidation = re.findall('id="__EVENTVALIDATION" value="([^\r\n]*)" ', content, re.S)[0]
		self.eco_viewstategenerator = re.findall('id="__VIEWSTATEGENERATOR" value="([^\r\n]*)" ', content, re.S)[0]

		## 第二次連線

		self.postData = {
			'__VIEWSTATE': self.eco_viewstate.decode('utf-8'),
			'__VIEWSTATEGENERATOR': self.eco_viewstategenerator.decode('utf-8'),
			'__EVENTVALIDATION': self.eco_eventvalidation.decode('utf-8'),
	        'DDL_YM': catchYear+','+catchSemester+'  ',
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
			print 'Department ' + str(department)
		
		## 第三次連線
		self.eco_viewstate = re.findall('id="__VIEWSTATE" value="([^\r\n]*)" />', content, re.S)[0]
		self.eco_eventvalidation = re.findall('id="__EVENTVALIDATION" value="([^\r\n]*)" ', content, re.S)[0]
		self.eco_viewstategenerator = re.findall('id="__VIEWSTATEGENERATOR" value="([^\r\n]*)" ', content, re.S)[0]
		self.postData = {
			'__VIEWSTATE': self.eco_viewstate.decode('utf-8'),
			'__VIEWSTATEGENERATOR': self.eco_viewstategenerator.decode('utf-8'),
			'__EVENTVALIDATION': self.eco_eventvalidation.decode('utf-8'),
	        'DDL_YM': catchYear+','+catchSemester+'  ',
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
			print 'Department ' + str(department)

		return content

	def parser(self, content):
		dom = BeautifulSoup(content, 'html.parser')
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
					courseData['code'] = rowData[1].text
					courseName = rowData[3].find_all('a')
					courseData['cname'] = courseName[0].text
					##courseData['ename'] = courseName[1].text
					courseData['time'] = rowData[5].text.replace('        ', ',')
					courseData['teacher'] = rowData[6].text
					courseData['year'] = 1041
					self.writeRow(courseData)
			except KeyError:
				continue


	
	def writeRow(self, row):
		##'ME108 A', '應用力學靜力', '1032', '何旭川(Shiuh-Chuan Her)', '106, 107, 108'
		##print type(str(row['time']))
		##self.database.write(u'(\''+row['code']+u'\','+u'\''+row['cname']+u'\','+u'\''+row['year']+u'\','+u'\''+row['teacher']+u'\','+u'\''+str(row['time'])+u'\'),')
		self.database.write(u'(')
		self.database.write(u'\''+row['code']+u'\', ')
		self.database.write(u'\''+row['cname']+u'\', ')
		self.database.write(u'\''+str(row['year'])+u'\', ')
		self.database.write(u'\''+row['teacher']+u'\', ')
		self.database.write(u'\''+row['time']+u'\'')
		self.database.write(u'), \r\n')

	def execute(self):
		for department in self.legalDepartment:
			self.parser(self.catch('104', '1', department, '0'))

		

courseCatcher = CourseCatcher()
courseCatcher.execute()