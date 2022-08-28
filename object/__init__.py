import os
path = os.getcwd() + '/object/'
__all__ = [i.replace('.py','')for i in os.listdir(path)]