'''
Auto signin or signout for NCKU check-in system

Usage:
    python auto_signin.py [option_type] [username] [password]
    [option_type]: can only be "signin" or "signout" 
    [username]   : NCKU ID
    [password]   : NCKU password

Author      : Chen, Wei-Han
Since       : 2016/08/23
Update notes:

'''

import requests
import json
import sys
import time
import datetime
import random


def main():
    special_day_list = load_special_day('special_day.txt')
    checkin = check_date(special_day_list)
    if checkin:
        print "Today is work day !"
    else:
        print "Today is holiday !"
        sys.exit()

    option    = sys.argv[1].lower()
    username  = sys.argv[2]
    passwd    = sys.argv[3]

    delay_min = 10.0

    if option=="signin":
        payload = {"Content-Type":"application/json", "data":{"fn":"signIn", "mtime":"A", "psnCode":username, "password":passwd}}
    elif option=="signout":
        payload = {"Content-Type":"application/json", "data":{"fn":"signIn", "mtime":"D", "psnCode":username, "password":passwd}}
    else:
        print '***ERROR: option_type can only be "signin" or "signout"'
        sys.exit()
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

    delay_time = random.random()*delay_min
    print "delay time: {0:5.2f} minutes".format(delay_time)
    time.sleep(delay_time*60)
    res = requests.post("http://eadm.ncku.edu.tw/welldoc/ncku/iftwd/doSignIn.php", json=payload, headers=head)

    if json.loads(res.text)['success']:
        print json.loads(res.text)['msg'].encode('utf8')
        if 'errorMsg' in json.loads(res.text).keys(): print json.loads(res.text)['errorMsg'].encode('utf8')
    else:
        print json.loads(res.text)['errorMsg'].encode('utf8')


def load_special_day(filename):
    special_day_list = []
    for line in open(filename, 'r'):
        year = int(line.split(' ')[0].split('/')[0])
        month = int(line.split(' ')[0].split('/')[1])
        day = int(line.split(' ')[0].split('/')[2])
        if line.strip().split(' ')[-1].lower() in 'holiday':
            special_day_list.append((year, month, day, 'h'))
        elif line.strip().split(' ')[-1].lower() in 'workday':
            special_day_list.append((year, month, day, 'w'))
    return special_day_list


def check_date(list):
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    current_day = datetime.datetime.now().day
    current_weekday = datetime.datetime.now().weekday()+1

    for date_year, date_month, date_day, date_type in list:
        if (current_weekday > 5):
            if (date_year == current_year and date_month == current_month and date_day == current_day and date_type == 'w'):
                return True
            else:
                return False
        else:
            if (date_year == current_year and date_month == current_month and date_day == current_day and date_type == 'h'):
                return False
            else:
                return True


main()
