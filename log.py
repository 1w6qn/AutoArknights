import time
class color:
    RED="\033[31m"
    WHITE="\033[37m"
    GREEN="\033[32m"
    YELLOW="\033[33m"
    BLUE="\033[34m"
    MAGENTA="\033[35m"
    RESET="\033[0m"
rcolor=[color.WHITE,color.GREEN,color.BLUE,color.MAGENTA,color.YELLOW,color.RED]
def d(data):
    msg=time.strftime("[%H:%M:%S]", time.localtime())+" "+data
    print(msg)
def e(data):
    msg=time.strftime("[%H:%M:%S]", time.localtime())+" "+data
    print(color.RED+msg+color.RESET)