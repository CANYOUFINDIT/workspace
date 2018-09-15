from bs4 import BeautifulSoup
import os


soup = BeautifulSoup(
    htmlhandle,
    'html.parser',
)

fieldset = soup.find('fieldset')
p = soup.find('p')
span = p.find_all('span')
count = 1
html = ""

for sp in span:
    if count != 7 and count != 8:
        html = html + str(sp)
    count = count + 1
html = html + str(fieldset)
print html