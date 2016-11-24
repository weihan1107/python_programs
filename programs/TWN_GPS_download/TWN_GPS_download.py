'''
Auto download Taiwan GPS data from CWB (Central Weather Bureau) 

Usage: python TWN_GPS_download.py [start_year] [start_doy] [end_year] [end_doy] 

Author      : Chen, Wei-Han
Since       : 2016/08/23
Update notes:

'''
import requests
from bs4 import BeautifulSoup
import datetime, sys

try:
    start_year = int(sys.argv[1]) 
    start_doy  = int(sys.argv[2]) 
    end_year   = int(sys.argv[3]) 
    end_doy    = int(sys.argv[4]) 
except IndexError:
    print "Usage: python TWN_GPS_download.py [start_year] [start_doy] [end_year] [end_doy]"
    sys.exit()

# doy to day
start_time = datetime.datetime(start_year, 1, 1) + datetime.timedelta(days=start_doy-1)
end_time   = datetime.datetime(  end_year, 1, 1) + datetime.timedelta(days=  end_doy-1)

# check time
if (end_time - start_time).days < 0:
    print "***ERROR: Input time have some problem, make sure that end_time larger than start_time."
    sys.exit()

# request header and payload
head={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
login_data = {'account':'family', 'pass':'770112', 'x':'10', 'y':'10'}
search_data={'search_day':'day', 'yearva':'2016', 'dayva':'1', 'dayvb':'1', 'yearv0':start_time.year, 'monthv0':start_time.month, 'dayv0':start_time.day, 'yearv1':end_time.year, 'monthv1':end_time.month, 'dayv1':end_time.day, 'station':'0', 'b_gps':'%B6%7D%A9l%ACd%B8%DF'}

# start to send request to server
s = requests.session()
response = s.post('http://gdms.cwb.gov.tw/login/member_login.php', data=login_data, headers=head) 
response = s.post('http://gdms.cwb.gov.tw/table-gps.php', data=search_data, headers=head)
soup = BeautifulSoup(response.text, 'lxml')
try:
    total_page = int(soup.select('.v')[0].strong.text)
except IndexError:
    total_page = 0
print "The search results have {0} page(s), and each page has at most 15 GPS data. ".format(total_page)
page_count = 1
data_count = 0
for page in range(total_page):
    response = s.get('http://gdms.cwb.gov.tw/table-gps.php?pageno={0}'.format(page+1))
    soup = BeautifulSoup(response.text, 'lxml')
    for target_line in soup.select('#dgEvents__ctl2_hlAsc1'):
        filename = target_line['href'][93:108]
        download_url = 'http://gdms.cwb.gov.tw/' + target_line['href'][21:-3]
        r = s.get(download_url)
        with open(filename, 'wb') as fid:
            fid.write(r.content)
        data_count += 1
    print "Process: {0}/{1}".format(page_count, total_page)
    page_count += 1

print "{0} GPS data have been download.".format(data_count)
