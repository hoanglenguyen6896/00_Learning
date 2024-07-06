# Need jupiter notebook

from ipywidgets import interact, interactive, fixed
import ipywidgets as widgets

def func(x):
    return x

# slider
interact(func, x=10)
# Checkbox
interact(func, x=True)
# TextBox, default 'hello'
interact(func, x="hello")

