from bs4 import BeautifulSoup

with open('hpoi.html', 'r') as f:
    contents = f.read()

    soup = BeautifulSoup(contents, "html.parser")

    for child in soup.descendants:

        if child.name:
            print(child.name)