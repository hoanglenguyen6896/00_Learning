"""
Import Modules (Like import .h file)
"""
from mymodules import my_func

my_func()

"""
Import Package
"""
import os
from mainpackage import mainScript
from mainpackage.subpackage import subScript

mainScript.main_report()

print(__file__)
print(os.path.join(os.path.dirname(__file__), '..'))
print(os.path.dirname(os.path.realpath(__file__)))
print(os.path.abspath(os.path.dirname(__file__)))