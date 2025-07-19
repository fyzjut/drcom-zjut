from time import sleep
import requests
import time
import os
import socket
import re
import getpass
import base64

# 自动登录文件的名称
AUTO_LOGIN_FILE = 'auto_login'

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

def check_network_connection():
    """使用HTTP请求检查网络连通性，替代ping命令"""
    test_urls = [
        "http://www.baidu.com",
        "http://www.qq.com"
    ]
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=5)
            # 检查是否收到有效响应 (状态码200或302)
            if response.status_code < 500:
                return True
        except:
            continue
    return False

def save_auto_login(username, password, ip):
    """保存自动登录信息（简单base64编码）"""
    # 组合用户名、密码和IP，用冒号分隔
    data = f"{username}:{password}:{ip}"
    encoded = base64.b64encode(data.encode()).decode()
    
    try:
        with open(AUTO_LOGIN_FILE, 'w') as f:
            f.write(encoded)
        print(f"自动登录信息已保存到 {AUTO_LOGIN_FILE}")
        print(f"如需取消自动登录，请删除 {AUTO_LOGIN_FILE} 文件")
    except Exception as e:
        print(f"保存自动登录信息失败: {str(e)}")

def load_auto_login():
    """加载自动登录信息"""
    if not os.path.exists(AUTO_LOGIN_FILE):
        return None, None, None
    
    try:
        with open(AUTO_LOGIN_FILE, 'r') as f:
            encoded = f.read().strip()
        # 解码并分割用户名、密码和IP
        decoded = base64.b64decode(encoded.encode()).decode()
        username, password, ip = decoded.split(':', 2)
        return username, password, ip
    except Exception as e:
        print(f"读取自动登录信息失败: {str(e)}")
        print("请手动输入登录信息")
        return None, None, None

def main():

    

    print("\n\033[94m==== 校园网认证助手 ====\033[0m")
    

    # 检查自动登录文件

    if os.path.exists(AUTO_LOGIN_FILE):

        print(f"检测到自动登录文件 {AUTO_LOGIN_FILE}")
        print(f"将使用保存的账号 [{auto_username}] 和IP [{auto_ip}] 自动登录")
        print(f"如需取消自动登录，请删除 {AUTO_LOGIN_FILE} 文件")
        # 读取信息
        auto_username, auto_password, auto_ip = load_auto_login()

        # 尝试自动登录
        # 自动登录成功，进入主循环
        login(auto_username, auto_password, auto_ip)
        cnt = 1
        sleep_time = 900
        try:
            while True:
                now = time.strftime("%Y-%m-%d %H:%M:%S")
                
                if check_network_connection():
                    print(f'\033[95m{now}\033[0m: \033[92m网络正常\033[0m')
                    sleep_time = 900
                else:
                    print(f'\033[95m{now}\033[0m: \033[91m网络断开，尝试重连 [{cnt}]\033[0m')
                    login(auto_username, auto_password, auto_ip)
                    sleep_time = 60
                    cnt += 1
                
                sleep(sleep_time)
        except KeyboardInterrupt:
            print("\n\033[93m程序终止，正在注销...\033[0m")
            logout(auto_ip)
        return
    
    # 交互式登录
    user_account = input("请输入校园网账号: ").strip()
    user_password = getpass.getpass("请输入密码: ").strip()
    local_ip = get_valid_ip()
        
    # 询问是否保存登录信息
    save_choice = input("下次自动登录? (y/n): ").strip().lower()
    if save_choice == 'y':
        save_auto_login(user_account, user_password, local_ip)
    
    # 首次登录尝试
    if not login(user_account, user_password, local_ip):
        print("\033[91m首次登录失败，请检查网络连接和账号信息\033[0m")
        return

    # 主循环
    cnt = 1
    sleep_time = 900
    
    try:
        while True:
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            
            if check_network_connection():
                print(f'\033[95m{now}\033[0m: \033[92m网络正常\033[0m')
                sleep_time = 900
            else:
                print(f'\033[95m{now}\033[0m: \033[91m网络断开，尝试重连 [{cnt}]\033[0m')
                login(user_account, user_password, local_ip)
                sleep_time = 60
                cnt += 1
            
            sleep(sleep_time)
    except KeyboardInterrupt:
        print("\n\033[93m程序终止，正在注销...\033[0m")
        logout(local_ip)

if __name__ == "__main__":
    main()
