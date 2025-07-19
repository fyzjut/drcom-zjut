from time import sleep
from subprocess import run, PIPE
import requests
import time
import os
import socket
import re
import getpass

def get_host_ip():
    """获取本机IP地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def login(user_account, user_password, local_ip):
    """登录校园网"""
    print(f'\033[95m{time.strftime("%Y-%m-%d %H:%M:%S")}\033[0m: '
          f'\033[94m登录账号 [{user_account}], IP [{local_ip}]\033[0m')
    
    # 新认证URL和参数
    url = 'http://192.168.6.1:801/eportal/'
    params = {
        'c': 'Portal',
        'a': 'login',
        'callback': 'dr1003',
        'login_method': 1,
        'user_account': user_account,
        'user_password': user_password,
        'wlan_user_ip': local_ip,
        'wlan_user_ipv6': '',
        'wlan_user_mac': '000000000000',
        'wlan_ac_ip': '192.168.6.36',
        'wlan_ac_name': 'ME60',
        'jsVersion': '3.3.3',
        'v': 6347
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        # 检查认证结果
        if '\\u8ba4\\u8bc1\\u6210\\u529f' in response.text or '认证成功' in response.text:
            print(f'\033[95m{time.strftime("%Y-%m-%d %H:%M:%S")}\033[0m: '
                  '\033[92m认证成功\033[0m')
            return True
        else:
            print(f'\033[95m{time.strftime("%Y-%m-%d %H:%M:%S")}\033[0m: '
                  '\033[91m认证失败，请检查账号密码\033[0m')
            return False
    except Exception as e:
        print(f'\033[95m{time.strftime("%Y-%m-%d %H:%M:%S")}\033[0m: '
              f'\033[91m连接失败: {str(e)}\033[0m')
        return False

def logout(local_ip):
    """注销校园网"""
    print(f'\033[95m{time.strftime("%Y-%m-%d %H:%M:%S")}\033[0m: '
          '\033[93m正在注销账号\033[0m')
    
    url = 'http://192.168.6.1:801/eportal/'
    params = {
        'c': 'Portal',
        'a': 'logout',
        'callback': 'dr1002',
        'login_method': 1,
        'user_account': 'drcom',
        'user_password': '123',
        'wlan_user_ip': local_ip,
        'jsVersion': '3.3.3',
        'v': 2603
    }
    
    try:
        requests.get(url, params=params, timeout=5)
    except:
        pass

def get_valid_ip():
    """获取有效的IP地址"""
    while True:
        auto_ip = get_host_ip()
        print(f"检测到本机IP: \033[93m{auto_ip}\033[0m")
        choice = input("使用该IP? (y/n): ").strip().lower()
        
        if choice == 'y':
            return auto_ip
        elif choice == 'n':
            manual_ip = input("请输入IP地址: ").strip()
            if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', manual_ip):
                return manual_ip
            print("\033[91mIP地址格式无效，请重新输入\033[0m")
        else:
            print("\033[91m请输入 y 或 n\033[0m")

def main():
    """主函数"""
    # 交互式登录
    print("\n\033[94m==== 校园网认证助手 ====\033[0m")
    user_account = input("请输入校园网账号: ").strip()
    user_password = getpass.getpass("请输入密码: ").strip()
    local_ip = get_valid_ip()
    
    # 首次登录尝试
    if not login(user_account, user_password, local_ip):
        print("\033[91m首次登录失败，请检查网络连接和账号信息\033[0m")
        return
    
    # 网络检测设置
    cnt = 1
    sleep_time = 600
    if os.name == "nt":
        cmdline = "ping www.baidu.com -n 3"
    else:
        cmdline = "ping www.baidu.com -c 3"
    
    # 主循环
    try:
        while True:
            r = run(cmdline, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            
            if r.returncode:
                print(f'\033[95m{now}\033[0m: '
                      f'\033[91m网络断开，尝试重连 [{cnt}]\033[0m')
                login(user_account, user_password, local_ip)
                sleep_time = 10
                cnt += 1
            else:
                print(f'\033[95m{now}\033[0m: \033[92m网络正常\033[0m')
                sleep_time = 60
            
            sleep(sleep_time)
    except KeyboardInterrupt:
        print("\n\033[93m程序终止，正在注销...\033[0m")
        logout(local_ip)

if __name__ == "__main__":
    main()
