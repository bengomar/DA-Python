from bs4 import BeautifulSoup as bs
import requests
import csv
import re
import urllib.request
import os

# lien de la page à scrapper
category_page_url = "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
lien = requests.get(category_page_url)
page = lien.content

# transforme (parse) le HTML en objet BeautifulSoup
soupe = bs(page, "html.parser")

# récupération des livres d'une catégorie donnée
#print(soup.find_all)
cherche_book = soupe.find_all('h3')

# création du fichier csv d'export avec les entetes uniquement
en_tete = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available',
            'product_description', 'category', 'review_rating', 'image_url']
with open('book_details.csv', 'a', newline="") as fichier_csv:
    obj = csv.DictWriter(fichier_csv, fieldnames=en_tete, delimiter=';')
    obj.writeheader()

for x in range(len(cherche_book)):
    cherche_book[x] = cherche_book[x].find('a', attrs={'href': re.compile("^../../..")})
    cherche_book[x] = cherche_book[x].get('href')
    cherche_book[x] = cherche_book[x].replace('../../..', 'http://books.toscrape.com/catalogue')


    # lien de la page d'un livre à scrapper

    product_page_url_var = cherche_book[x]
    response = requests.get(product_page_url_var)
    html = response.content

    # transforme (parse) le HTML en objet BeautifulSoup
    soup = bs(html, "html.parser")

    # récupération du  titre du livre
    title_var = soup.find('h1').string

    # récupération des détails du livre entre les balises <td>
    cherche_td = soup.find_all('td')
    book_data = []
    for td in cherche_td:
        book_data.append(td.string)

    # dictionnaire des détails du livre
    book_data[3] = book_data[3].replace('£', '')
    book_data[2] = book_data[2].replace('£', '')
    book_data[5] = book_data[5].replace('In stock (', '')
    book_data[5] = book_data[5].replace(' available)', '')
    detail_livre = {'upc': book_data[0], 'price_including_tax': book_data[3], 'price_excluding_tax': book_data[2], 'number_available': book_data[5]}

    # récupération de la description du livre, balise <meta>
    cherche_meta = soup.find_all("meta")
    meta_description = []
    for meta in cherche_meta:
       meta_description.append(meta)
    prod_meta_desc = meta_description[2].get('content')
    product_description_var = prod_meta_desc.strip()
    
    # récupération de la catégorie, balise <a href>
    cherche_a = soup.find_all('a')
    book_categorie = []
    for a in cherche_a:
       book_categorie.append(a)
    category_var = book_categorie[3].string
    
    # récupération du nombre d'étoile assigné au livre, balise <p class="star-rating ...>
    map_rating = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    cherche_p = soup.select('p.star-rating')
    element_rating = cherche_p[0]
    rating_class_number = element_rating['class'][1]
    review_rating_var = map_rating[rating_class_number]

    # récupération de l'image de la couverture du livre
    cherche_thumbnail = soup.find('img')['src']
    image_url_var = cherche_thumbnail.replace('../..', 'http://books.toscrape.com')
    path_categories = f'./categories/{category_var}/images/'
    os.makedirs(path_categories, exist_ok=True)
    image_name = product_page_url_var.replace('http://books.toscrape.com/catalogue/', '')
    image_name = image_name.replace('/index.html', '')
    path_image = f'{path_categories}{image_name}.jpg'
    #urllib.request.urlretrieve(image_url_var, f"{path_categories}{image_name}.jpg")
    urllib.request.urlretrieve(image_url_var, path_image)

    print(f"{product_page_url_var=}")
    print(f"{detail_livre['upc']=}")
    print(f"{title_var=}")
    print(f"{detail_livre['price_including_tax']=}")
    print(f"{detail_livre['price_excluding_tax']=}")
    print(f"{detail_livre['number_available']=}")
    print(f"{product_description_var=}")
    print(f"{category_var=}")
    print(f"{review_rating_var=}")
    print(f"{image_url_var=}")
    print(f"{path_image=}")

    # exportation de données vers un fichier csv

    with open('book_details.csv', 'a', newline="") as fichier_csv:
        obj = csv.DictWriter(fichier_csv, fieldnames=en_tete, delimiter=';')
       # obj.writeheader()
        obj.writerow({'product_page_url': product_page_url_var, 'upc': detail_livre['upc'], 'title': title_var,
                     'price_including_tax': detail_livre['price_including_tax'],
                     'price_excluding_tax': detail_livre['price_excluding_tax'],
                     'number_available': detail_livre['number_available'],
                     'product_description': product_description_var, 'category': category_var,
                     'review_rating': review_rating_var, 'image_url': image_url_var})
