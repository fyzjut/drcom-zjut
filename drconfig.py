#
#
#
#
#
# Example:
# self.local_ip='10.11.1.1'
# self.user_account = "2111000001"
# self.user_password = "password" 
import socket

class LoginInfo:
    def get_host_ip():
        """
        查询本机ip地址
        :return: ip
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip


    def __init__(self):
        Use_router=True
        if Use_router:
            self.local_ip=''
        else:
            self.local_ip=LoginInfo.get_host_ip()
        self.user_account=''
        self.user_password=''
