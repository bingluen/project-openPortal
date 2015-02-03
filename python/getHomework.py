username = 's1010541'
password = '09er33ic88ks27on24'


import requests
import re

r = requests.Session()

content = r.post('https://portalx.yzu.edu.tw/PortalSocialVB/Login.aspx').text


ecoVIEWSTATEGENERATOR = re.findall('__VIEWSTATEGENERATOR id="__VIEWSTATEGENERATOR" value="([^"]*)"', content, re.S)
ecoVIEWSTATE = re.findall('__VIEWSTATE" id="__VIEWSTATE" value="([^"]*)"', content, re.S)
ecoEVENTVALIDATION = re.findall('__EVENTVALIDATION" id="__EVENTVALIDATION" value="([^"]*)"', content, re.S)

postdata={
    '__VIEWSTATE':ecoVIEWSTATE,
    '__VIEWSTATEGENERATOR':ecoEVENTVALIDATION,
    '__EVENTVALIDATION':ecoEVENTVALIDATION,
    'Txt_UserID':username,
    'Txt_Password':password,
    'ibnSubmit':'\xe7\x99\xbb\xe5\x85\xa5'
}


login_result = r.post('https://portalx.yzu.edu.tw/PortalSocialVB/Login.aspx', data=postdata, verify=False).text

###get portal homepage after login
content = r.get('https://portalx.yzu.edu.tw/PortalSocialVB/FMain/DefaultPage.aspx?Menu=Default').text


###get all of course

content = r.get('https://portalx.yzu.edu.tw/PortalSocialVB/FMain/PageByDuty.aspx?DutyType=std').text

print(content)
