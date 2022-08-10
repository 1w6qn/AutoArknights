class NetworkError(Exception):
    def __init__(self,msg):
        self.msg=msg
    def __str__(self):
        return f"网络错误:{self.msg}"