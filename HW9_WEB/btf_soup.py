import json
import requests
from bs4 import BeautifulSoup
import re

url = "http://quotes.toscrape.com/"
author_list =[]
quote_list =[]


def find_quotes():

    i = 1
    while True:
        html_doc = requests.get(f"{url}page/{i}/")
        soup = BeautifulSoup(html_doc.text, 'lxml')
        if not re.findall('No quotes found', html_doc.text):
            i +=1
        else: break

        for quote in soup.find_all("div", class_="quote"):
            text = quote.find("span", class_="text").get_text()
            tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]
            author = quote.find("small", class_="author").get_text().strip()
            author_url = quote.find("a", href=True).get('href').lstrip('/')

            quote_list.append({
                "tags": tags,
                "author": author,
                "quote": text
            })

            if author_url not in author_list:
                author_list.append(author_url)

    with open("quotes.json", "w", encoding='utf-8') as f:
        json.dump(quote_list, f, ensure_ascii=False, indent=4)

def find_authors():

    authors_info = []
    for author in author_list:
        html_doc = requests.get(f"{url}{author}")
        soup = BeautifulSoup(html_doc.text, 'lxml')

        fullname = soup.find("h3", class_="author-title").get_text().strip()
        born_date = soup.find("span", class_="author-born-date").get_text().strip()
        born_location = soup.find("span", class_="author-born-location").get_text().strip()
        description = soup.find("div", class_="author-description").get_text().strip()

        authors_info.append({
            "fullname": fullname,
            "born_date": born_date,
            "born_location": born_location,
            "description": description
        })

    with open("authors.json", "w", encoding='utf-8') as f:
        json.dump(authors_info, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    find_quotes()
    find_authors()