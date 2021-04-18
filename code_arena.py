"""
[*a] = "RealPython"
print(a)

from collections import namedtuple
from typing import Callable


City = namedtuple('City' , 'name population')

c1 = City('Bratislava', 432000)
c2 = City('Budapest', 1759000)

name, population = c1
# population, name = c1
print(f'{name}: {population}')

print('----------------------')

print(c2)
print(*c2)
# print(*c2, sep=': ')


thistuple = tuple(("corn", "apple", "banana", "cherry")) # note the double round-brackets
print(sorted(thistuple, key=None, reverse=True))


a, b = 1, 2
print(a+b)

fruits = ["apple", "banana", "cherry"]
veggies = ["tomato", "spinach", "potato"]
for x, y in enumerate(fruits):
    print(x)
    print(y)
"""

from bs4 import BeautifulSoup
from collections import namedtuple
import urllib
import json
import requests

url = "http://www.runescape.com"
r = urllib.request.urlopen(url).read()  # extracts html structure from url
#print(r)

soup = BeautifulSoup(r, features="lxml")  # readable format via bs4
s_title = soup.title
s_script = soup.script

print("<--------------------------------------------------------->")
print(soup)
print("<--------------------------------------------------------->")
print(s_title)
print("<--------------------------------------------------------->")
print(s_script)
print("<--------------------------------------------------------->")
Thing = namedtuple('Thing', ['name', 'value', 'weight'])

things = [
    Thing('Water Bottle', 30, 192),
    Thing('Notepad', 40, 333),
    Thing('Coffee Mug', 60, 350),
    Thing('Headphones', 150, 160),
    Thing('Laptop', 500, 2200)
]

print(things[0])
#print(soup.title)
#print(soup.a)

