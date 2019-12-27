import os
from lxml import etree
from bs4 import BeautifulSoup
import re
import requests
import itertools
import difflib


def xpath_soup(element):
    """
    Generate xpath of soup element
    :param element: bs4 text or node
    :return: xpath as string
    """
    components = []

    child = element if element.name else element.parent

    _xpath = {"path": "", "node": []}

    for parent in child.parents:

        """
        @type parent: bs4.element.Tag
        """
        previous = itertools.islice(
            parent.children, 0, parent.contents.index(child))

        xpath_tag = child.name
        cnt = sum(1 for i in child.parent.children)
        xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1

        components.append(xpath_tag if xpath_index ==
                          0 else '%s[%d]' % (xpath_tag, xpath_index))
        child = parent
        _xpath['node'].append(xpath_index)

    components.reverse()

    _xpath['path'] = '/%s' % '/'.join(components)
    return _xpath


def replace_between(text, begin, end, alternative=''):
    middle = text.split(begin, 1)[1].split(end, 1)[0]
    return text.replace(middle, alternative)

# demo1
# url = "https://investors.fiserv.com/corporate-information/executive-committee"
# name1 = "Jeffery W. Yabuki"
# name2 = "Christopher  M. Foskett"


# demo2
# url = "https://www.confluent.io/about#about_confluent"
# name1 = "Jay Kreps"
# name2 = "Neha Narkhede"

url = "https://www.jianshu.com/search?q=python&page=1&type=collection"
name1 = "Pythoner集中营"
name2 = "我的Python自学之路"

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    "Content-Type": "application/json;charset=UTF-8",
    "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7"
}

request = requests.get(url=url, headers=headers)

if request.status_code != 200:
    print(request.status_code)
    print(request.text)
    os._exit(0)

html = request.text

soup = BeautifulSoup(html, 'lxml')
elem = soup.find(string=re.compile(name1))

if elem == None:
    print("Missing Name1")
    os._exit(0)

xpath1 = xpath_soup(elem)

elem = soup.find(string=re.compile(name2))

if elem == None:
    print("Missing Name2")
    os._exit(0)

xpath2 = xpath_soup(elem)

d = difflib.Differ()
s = difflib.SequenceMatcher(None, xpath1['path'], xpath2['path'])

for op in s.get_opcodes():
    if op[0] == "replace":
        start = op[1]
        end = op[2]

xpath_model = xpath1['path'][:start]+"$1"+xpath1['path'][end:]

xpath_model = re.sub(r'\[[0-9]*\$1\]','[$1]',xpath_model)

print(xpath_model)

parent_xpath = xpath_model.split("[$1]")

selector = etree.HTML(html)





parent_nodes = selector.xpath(parent_xpath[0])

_range = len(parent_nodes)

res_names = []
for i in range(1, _range):
    fixed_path = xpath_model.replace(
        "$1", str(i))+"/text()"
    texts = selector.xpath(fixed_path)
    for text in texts:
        if text.strip() != "":
            res_names.append(text.strip())

print(res_names)
