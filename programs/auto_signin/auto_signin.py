'''
Auto signin or signout for NCKU check-in system


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
import optparse


def main():
    opts, args = opt_control()
    option, username, passwd = args
    now_time = datetime.datetime.now()
    special_day_list = load_special_day(opts)
    checkin = check_date(special_day_list, now_time)
    if checkin:
        if option == 'signin': print_information(opts.output_filename, "{0}/{1:02}/{2:02}: Today need to work  :(".format(now_time.year, now_time.month, now_time.day))
    else:
        if option == 'signin':
            print_information(opts.output_filename,  "{0}/{1:02}/{2:02}: Today no need to work :)\n".format(now_time.year, now_time.month, now_time.day) + "-"*50)
        sys.exit()

    delay_min = float(opts.delay_time)

    if option == "signin":
        payload = {"Content-Type":"application/json", "data":{"fn":"signIn", "mtime":"A", "psnCode":username, "password":passwd}}
    elif option == "signout":
        payload = {"Content-Type":"application/json", "data":{"fn":"signIn", "mtime":"D", "psnCode":username, "password":passwd}}
    else:
        print_information(opts.output_filename,  '***ERROR: option_type can only be "signin" or "signout"')
        sys.exit()
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

    delay_time = random.random()*delay_min
    time.sleep(delay_time*60)
    res = requests.post("http://eadm.ncku.edu.tw/welldoc/ncku/iftwd/doSignIn.php", json=payload, headers=head)

    if json.loads(res.text)['success']:
        print_information(opts.output_filename, json.loads(res.text)['msg'].encode('utf8'))
        if 'errorMsg' in json.loads(res.text).keys(): print_information(opts.output_filename, json.loads(res.text)['errorMsg'].encode('utf8'))
    else:
        print_information(opts.output_filename, json.loads(res.text)['errorMsg'].encode('utf8'))

    if option == 'signout':
        print_information(opts.output_filename, "-"*50)


def load_special_day(opts):
    filename = opts.special_day_filename
    if filename is None:
        print_information(opts.output_filename, "***ERROR: flag [-s] must be set a file!")
        sys.exit()
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


def check_date(list, now_time):
    current_year = now_time.year
    current_month = now_time.month
    current_day = now_time.day
    current_weekday = now_time.weekday()+1

    if (current_weekday > 5):
        for date_year, date_month, date_day, date_type in list:
            if (date_year == current_year and date_month == current_month and date_day == current_day and date_type == 'w'):
                return True
        return False
    else:
        for date_year, date_month, date_day, date_type in list:
            if (date_year == current_year and date_month == current_month and date_day == current_day and date_type == 'h'):
                return False
        return True


def opt_control():
    parser = optparse.OptionParser(usage="usage: %prog [options] [signin/signout] [username] [password]")
    parser.add_option("-d", default=0, dest="delay_time", help="set up the delay time (unit: minutes, default: 0)")
    parser.add_option("-s", default=None, dest="special_day_filename", help="assign a special day file")
    parser.add_option("-o", default=None, dest="output_filename", help="assign a output file to print information")
    opts, args = parser.parse_args()
    return opts, args


def print_information(filename, msg):
    if filename is None:
        print msg
    else:
        with open(filename, 'a') as fid:
            fid.write(msg+'\n')


main()
