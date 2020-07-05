# coding=utf-8

from bs4 import BeautifulSoup
import re

f = open("./baidu.html", "rb")
html = f.read()
bs = BeautifulSoup(html, "html.parser")

# print(bs.a)

t_list = bs.find_all(re.compile("a"))
print(t_list)