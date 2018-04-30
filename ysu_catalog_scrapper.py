# David Ariyibi, Williams College, daa1@williams.edu
# Katherine Blake, Williams College, kbb2@williams.edu
# Anthony Simpson, Williams College, als7@williams.edu
from bs4 import BeautifulSoup
import requests
import json

site = "http://catalog.ysu.edu/courses/"
base = "http://catalog.ysu.edu"

def getLinks():
    page = requests.get(site)
    soup = BeautifulSoup(page.content, "html.parser")

    a_elements = soup.find('div', attrs = {'id': 'atozindex'}).find_all('a')

    div_info =[]

    for a in a_elements:
        text = a.get_text()
        text = text.replace(')', '')
        div = text.split(' (')
        div.append(a['href'])
        div_info.append(div)

    return div_info

def scrape_division_page(link):
    page = requests.get(base+link)
    soup = BeautifulSoup(page.content, "html.parser")

    course_elements = soup.find_all('div', attrs = {'class': 'courseblock'})

    div_info = {}

    for course in course_elements:
        cb_title = course.find('p', attrs = {'class': 'courseblocktitle'})
        cb_title_text = cb_title.get_text()
        cb_title_text = cb_title_text.replace('s.h.', '')
        cb_title_text = removeUnicode(cb_title_text)
        cb_title = cb_title_text.split(' ')


        index = len(cb_title) - 5
        num = ' '.join(cb_title[0:2])
        name = ' '.join(cb_title[5:index]) # change from 2 -> 5 removes extra space from beginning of course name
        credits = cb_title[len(cb_title)-2]

        cb_description = course.find('p', attrs = {'class': 'courseblockdesc'})
        cb_description = cb_description.get_text().split('Prereq.: ')

        description = cb_description[0]
        description = description[2:] # removes '\n ' from beginning of course description
        prereq = 'None'

        if (len(cb_description) > 1):
            prereq = cb_description[1]
            prereq = removeUnicode(prereq) # removes Unicode from any courses listed in a course's prereq

        course_info = {'number': num, 'name': name, 'credit hours': credits,
                        'description': description, 'prereq': prereq}

        div_info[num] = course_info

    return div_info

def scrape_catalog():
    div_info = getLinks()
    catalog = {}

    for div in div_info:
        catalog[div[1]] = {'division': div[0], 'link': div[2]}
        catalog[div[1]]['classes'] = scrape_division_page(div[2])

    save(catalog, 'YSU_catalog')

def save(info, name):
    name = removeUnicode(name)
    name = name.replace('/', '-')
    with open(name + '.json', 'w') as fp:
        json.dump(info, fp, indent=4)


def removeUnicode(text):
    return (''.join([i if ord(i) < 128 else ' ' for i in text])).encode('ascii', 'ignore')

def load(name):
    with open(name + '.json', 'r') as fp:
        return json.load(fp)

if __name__ == '__main__':
    scrape_catalog()
