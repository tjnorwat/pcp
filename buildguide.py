import json
import requests
from bs4 import BeautifulSoup


def writeJson(data: dict) -> None:
    with open('cogs/json_guides/buildguide.json', 'w') as f:
        json.dump(data, f)


#  condense gpu text to just the model
def gpuText(text: str) -> str:
    words = text.split(' ')
    for i in range(len(words) - 1):
        if words[i].lower() in ['radeon', 'geforce']:
            string = words[i] + ' ' + words[i + 1] + ' ' + words[i + 2]
            if string.endswith(';') or string.endswith(')'):
                return string[:-1]
            return string
    return 'None'


# condense cpu text to just the model
def cpuText(text: str) -> str:
    return ' '.join(text.split()[1:])


# condense price text to just the price
def priceText(text: str) -> int:
    num = text.replace('$', '').replace('+', '')
    return int(float(num))


# refresh build guide data
def updateBuildGuide():
    guide_list = []
    r = requests.get("https://pcpartpicker.com/guide/")
    soup = BeautifulSoup(r.text, 'lxml')
    guides = soup.find_all('li', {'class' : 'guideGroup guideGroup__card'})

    for guide in guides:
        data = {}
        title = guide.find('h1', {'class' : 'guide__title'}).get_text()
        link = guide.a.get('href')

        price = guide.find('p', {'class' : 'guide__price'}).get_text().strip()

        un_list = guide.find('ul', {'class' : 'guide__keyProducts list-unstyled'})
        cpu = un_list.li.get_text()
        gpu = un_list.li.next_sibling.next_sibling.get_text()
        
        data['title'] = title
        data['link'] = 'https://pcpartpicker.com' + link
        data['cpu'] = cpuText(cpu)
        data['gpu'] = gpuText(gpu)
        data['price'] = priceText(price)

        guide_list.append(data)

    writeJson(guide_list)


if __name__ == '__main__':
    updateBuildGuide()
