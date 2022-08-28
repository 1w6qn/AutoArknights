import os
path = os.getcwd() + '/dev/'
__all__ = [i.replace('.py','')for i in os.listdir(path)]
from dev import *