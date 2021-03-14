import json
import requests
from bs4 import BeautifulSoup


def writeJson(data: dict) -> None:
    with open('cogs/json_guides/completedguide.json', 'w') as f:
        json.dump(data, f)


# condense cpu text to just the model
def cpuText(text: str) -> str:
    s = ' '.join(text.split()[1:])
    if '@' in s:
        return ' '.join(s.split()[:2])
    return s


# condense price text to just the price
def priceText(text: str) -> int:
    num = text.replace('$', '').replace('+', '')
    return int(float(num))


def parseData(guide_list: list, builds):
    for build in builds:
        data = {}
        title = build.find('h1', {'class' : 'log__title'}).a.get_text()
        link = build.a.get('href')

        price = build.find('p', {'class' : 'log__price'}).get_text()

        un_list = build.find('ul', {'class' : 'log__keyProducts list-unstyled'})
        cpu = un_list.li.get_text()

        try:
            gpu = un_list.li.next_sibling.next_sibling.get_text()
        except AttributeError:
            gpu = 'None'
        data['title'] = title
        data['link'] = 'https://pcpartpicker.com' + link
        data['cpu'] = cpuText(cpu)
        data['gpu'] = gpu
        data['price'] = priceText(price)

        guide_list.append(data)


def updateCompleteGuide():
    guide_list = []

    s = requests.Session()
    r = s.get('http://pcpartpicker.com/builds')
    token = s.cookies['xcsrftoken']
    headers = {
            'referer' : 'https://pcpartpicker.com/builds/',
            'X-CSRFToken' : token
        }

    data = {
            'page' : '1',
            'period' : '1w'
        }

    # get the first page of completed guides
    r = s.post("https://pcpartpicker.com/builds/fetch/", data=data, headers=headers)
    html = json.loads(r.text)
    soup = BeautifulSoup(html['result']['html'], 'lxml')
    builds = soup.find_all('li', {'class' : 'logGroup logGroup__card'})

    parseData(guide_list, builds)

    # have to find total number of pages from a different key 
    page_soup = BeautifulSoup(html['result']['paging_row'], 'lxml')
    un_list = page_soup.find('ul', {'class' : 'pagination list-unstyled xs-text-center'})
    pages = un_list.find_all('li')
    total_pages = int(pages[-1].a.get_text())

    # iterate through the rest of the pages and parse data
    for i in range(2, total_pages + 1):
        data = {
            'page' : i,
            'period' : '1w'
        }
        r = s.post("https://pcpartpicker.com/builds/fetch/", data=data, headers=headers)
        html = json.loads(r.text)
        soup = BeautifulSoup(html['result']['html'], 'lxml')
        builds = soup.find_all('li', {'class' : 'logGroup logGroup__card'})
        parseData(guide_list, builds)

    writeJson(guide_list)


if __name__ == '__main__':
    updateCompleteGuide()
