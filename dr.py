from time import sleep
from subprocess import run, PIPE
import requests
import time
import os
from drconfig import LoginInfo

_l=LoginInfo()

def login():
    
    print('\033[95m{}\033[0m\033[94m: Logging to [{}],IP [{}]\033[0m'.format(time.strftime("%Y-%m-%d %H:%M:%S"),_l.user_account,_l.local_ip))
    url='http://a.zjut.edu.cn:801/eportal/?c=Portal&a=login&callback=dr1003&login_method=1&user_account={}&user_password={}&wlan_user_ip={}&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=3.3.3&v=2440'.format(_l.user_account,_l.user_password,_l.local_ip)
    try:
        requests.post(url)
    except:
        
        print('\033[95m{}\033[0m: \033[91mFail to connect, network is down. \033[0m'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
        pass
def logout():
    print('\033[95m{}\033[0m: 正在注销账号[\033[94m{}\033[0m],IP [\033[93m{}\033[0m]'.format(time.strftime("%Y-%m-%d %H:%M:%S"),_l.user_account,_l.local_ip))
    url = 'http://a.zjut.edu.cn:801/eportal/?c=Portal&a=logout&callback=dr1002&login_method=1&user_account=drcom&user_password=123&ac_logout=0&register_mode=1&wlan_user_ip={}&wlan_user_ipv6=&wlan_vlan_id=1&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=3.3.3&v=2603'.format(_l.local_ip)
    requests.post(url)



cnt = 1
sleep_time=0

login() #Connect

if(os.name=="nt"):
    cmdline="ping www.baidu.com"
else:
    cmdline="ping www.baidu.com -c 3"

while True:
    r = run(cmdline,
            stdout=PIPE,
            stderr=PIPE,
            stdin=PIPE,
            shell=True)
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    if r.returncode:
        print('\033[95m{}\033[0m: \033[91mNetwork disconnected，Reconnection times[{}].\033[0m'.format(now,cnt))
        login()
        sleep_time=10
        cnt += 1
    else:
        print('\033[95m{}\033[0m: \033[92mNetwork connected \033[0m'.format(now))
        sleep_time=60

    sleep(sleep_time) # 每x秒检查一次

