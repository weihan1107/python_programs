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
import json, sys
import time, random

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

