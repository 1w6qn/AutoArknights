import os
path = os.getcwd() + '/object/'
files = os.listdir(path)
__all__ = []
for i in files:
    __all__.append(i.replace('.py', ''))
