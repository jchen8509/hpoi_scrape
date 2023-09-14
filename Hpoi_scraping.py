import requests
from bs4 import BeautifulSoup, Tag, ResultSet
from dataclasses import dataclass

URL = "https://www.hpoi.net"
wait_time_seconds:float = 60 * 5
# Chinese translations
translations = {
    "Name": '名称',
    "Origin": '作品',
    "Character": '角色',
    "Manufacturer": '制作',
    "Illustrator": '原画',
    "Release Date": '发售日',
    "Price": '定价',
    "Material": '材质',
    "Scale": '比例',
    "Dimension": '尺寸'
}
# number of cards to poll at once
batch_size = 5

# TODO: add consts for selectors
@dataclass
class hpoiCard:
    # --OUTER PAGE--
    # update title
    title: str
    # update status
    status: str
    # description for update status
    status_description: str
    # full link to item page
    link: str
    img_src: str

    # --INNER PAGE--
    name: str
    origin: str
    character: str
    manufacturer: str
    illustrator: str
    release_date: str
    price: str
    material: str
    scale: str
    dimension: str

    ## def __str__(self):
    ##    return 'TODO'

def tag_to_card(tag: Tag) -> hpoiCard: 
    # --OUTER PAGE--
    image:Tag = tag.find("div", class_="left-leioan").find("a")
    info:Tag = tag.find("div", class_="right-leioan")

    title:str = info.find_all("div")[4].text
    status:str = info.find("div").find("span").text
    status_description:str = info.find_all("div")[3].text
    link:str = URL + "/" + image.get("href")
    img_src:str = image.find("img").get("src")

    # --INNER PAGE--m
    page = requests.get(link)
    inner_soup = BeautifulSoup(page.content, "html.parser")

    inner_info:Tag = inner_soup.find("div", class_= "infoList-box")
    
    name = getItem(inner_info, translations.get("Name"))
    origin = getItem(inner_info, translations.get("Origin"))
    character = getItem(inner_info, translations.get("Character"))
    manufacturer = getItem(inner_info, translations.get("Manufacturer"))
    illustrator = getItem(inner_info, translations.get("Illustrator"))
    release_date = getItem(inner_info, translations.get("Release Date"))
    price = getItem(inner_info, translations.get("Price"))
    material = getItem(inner_info, translations.get("Material"))
    scale = getItem(inner_info, translations.get("Scale"))
    dimension = getItem(inner_info, translations.get("Dimension"))

    return hpoiCard(title, status, status_description, link, img_src, 
                    name, origin, character, manufacturer, illustrator,
                    release_date, price, material, scale, dimension)
                    
# Grabs text of info list item safely
def getItem(tag: Tag, infoList_name: str):
    try:
        return tag.find("span", string = infoList_name).findNext('p').text
    except AttributeError:
        print(infoList_name + ' not found')
        return "N/A"
    
titleCache: list[str] = []

def fetchCards() -> list[hpoiCard]:    
    print('Loading page...')
    page = requests.get(URL)
    print('Page loaded!')
    soup = BeautifulSoup(page.content, "html.parser")

    tags: ResultSet[Tag] = soup.find("div", class_="hpoi-conter-ltsifrato").find_all("div", class_="hpoi-conter-left")

    tags = tags[:batch_size]

    titles = map(lambda tag: tag.find("div", class_="right-leioan").find_all("div")[4].text, tags)
    tags_and_titles = zip(tags,titles)
    tags_and_titles = list(filter(lambda pair: pair[1] not in titleCache, tags_and_titles))

    if(len(tags_and_titles) <= 0):
        print("Found no new cards!")
        return []
    print("Found "+str(len(tags_and_titles))+ " new cards!")

    cards: list[hpoiCard] = []
    for tag, title in tags_and_titles:
        # code to grab card data
        cards.append(tag_to_card(tag))
        titleCache.append(title)
        
    return cards

if __name__ == "__main__":
    fetchCards()
