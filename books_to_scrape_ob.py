import csv
import os
import re
from urllib.request import urlretrieve

import requests
from bs4 import BeautifulSoup as bs


def scrape_book(page_url: str) -> dict:
    """Fonction qui récupère toutes les données pour un livre et les écrit dans un fichier csv"""

    response = requests.get(page_url)
    html = response.content

    # transforme (parse) le HTML en objet BeautifulSoup
    soup = bs(html, "html.parser")

    # récupération du titre du livre
    title_var = soup.find("h1").string

    # récupération des détails du livre entre les balises <td>
    cherche_td = soup.find_all("td")
    book_data = []
    for td in cherche_td:
        book_data.append(td.string)

    # dictionnaire des détails du livre
    book_data[3] = book_data[3].replace("£", "")
    book_data[2] = book_data[2].replace("£", "")
    book_data[5] = book_data[5].replace("In stock (", "")
    book_data[5] = book_data[5].replace(" available)", "")
    detail_livre = {
        "upc": book_data[0],
        "price_including_tax": book_data[3],
        "price_excluding_tax": book_data[2],
        "number_available": book_data[5],
    }

    # récupération de la description du livre, balise <meta>
    cherche_meta = soup.find_all("meta")
    meta_description = []
    for meta in cherche_meta:
        meta_description.append(meta)
    prod_meta_desc = meta_description[2].get("content")
    product_description_var = prod_meta_desc.strip()

    # récupération de la catégorie, balise <a href>
    cherche_a = soup.find_all("a")
    book_categorie = []
    for a in cherche_a:
        book_categorie.append(a)
    category_var = book_categorie[3].string

    # récupération du nombre d'étoiles assigné au livre (balise <p class="star-rating ...>)
    map_rating = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    cherche_p = soup.select("p.star-rating")
    element_rating = cherche_p[0]
    rating_class_number = element_rating["class"][1]
    review_rating_var = map_rating[rating_class_number]

    # récupération de l'image de la couverture du livre
    cherche_thumbnail = soup.find("img")["src"]
    image_url_var = cherche_thumbnail.replace("../..", "http://books.toscrape.com")
    path_categories = f"./categories/{category_var}/images/"
    os.makedirs(path_categories, exist_ok=True)
    image_name = page_url.replace("http://books.toscrape.com/catalogue/", "")
    image_name = image_name.replace("/index.html", "")
    path_image = f"{path_categories}{image_name}.jpg"
    path_image_errno_36 = f"{path_categories}{title_var[:130]}....jpg"

    print(
        f"-------Start scraping product page of book: {title_var}------------------------------->"
    )
    print(f"{page_url=}")
    print(f"{detail_livre['upc']=}")
    print(f"{title_var=}")
    print(f"{detail_livre['price_including_tax']=}")
    print(f"{detail_livre['price_excluding_tax']=}")
    print(f"{detail_livre['number_available']=}")
    print(f"{product_description_var=}")
    print(f"{category_var=}")
    print(f"{review_rating_var=}")
    print(f"{image_url_var=}")

    # Permet de gérer l'OSError: [Errno 36] File name too long'
    try:
        urlretrieve(image_url_var, path_image)
    except OSError as exc:
        if exc.errno == 36:
            urlretrieve(image_url_var, path_image_errno_36)
            print(f"{path_image_errno_36=}")
            print(
                "--------------------------------------------------------------------------------------->"
            )

        else:
            print(f"{path_image=}")
            print(
                "--------------------------------------------------------------------------------------->"
            )
            raise

    # exportation de données vers un fichier csv
    en_tete = [
        "product_page_url",
        "upc",
        "title",
        "price_including_tax",
        "price_excluding_tax",
        "number_available",
        "product_description",
        "category",
        "review_rating",
        "image_url",
    ]
    with open(
        f"./categories/{category_var}/{category_var}_details.csv", "a", newline=""
    ) as file_csv:
        obj = csv.DictWriter(file_csv, fieldnames=en_tete, delimiter=";")
        obj.writerow(
            {
                "product_page_url": page_url,
                "upc": detail_livre["upc"],
                "title": title_var,
                "price_including_tax": detail_livre["price_including_tax"],
                "price_excluding_tax": detail_livre["price_excluding_tax"],
                "number_available": detail_livre["number_available"],
                "product_description": product_description_var,
                "category": category_var,
                "review_rating": review_rating_var,
                "image_url": image_url_var,
            }
        )

    return detail_livre


def scrape_books(url_category: str) -> dict:
    """Fonction qui récupère toutes les url des livres pour une catégorie"""

    # lien de la page à scrapper
    lien = requests.get(url_category)
    page = lien.content

    # transforme (parse) le HTML en objet BeautifulSoup
    soupe = bs(page, "html.parser")

    # récupération des livres d'une catégorie donnée
    # print(soup.find_all)
    cherche_book = soupe.find_all("h3")

    for x in range(len(cherche_book)):
        cherche_book[x] = cherche_book[x].find(
            "a", attrs={"href": re.compile("^../../..")}
        )
        cherche_book[x] = cherche_book[x].get("href")
        cherche_book[x] = cherche_book[x].replace(
            "../../..", "http://books.toscrape.com/catalogue"
        )

        # lien de la page d'un livre à scrapper

        scrape_book(cherche_book[x])


def run_scraping():
    # liens des pages à scrapper
    product_page_url_var = "http://books.toscrape.com/index.html"
    response = requests.get(product_page_url_var)
    html = response.content

    # transforme (parse) le HTML en objet BeautifulSoup
    soup = bs(html, "html.parser")

    # récupération des catégories balise <a> avec présence de href
    cherche_cat = soup.find_all("a", href=True)
    del cherche_cat[0:3]
    del cherche_cat[50:91]

    # recupération des noms de catégories
    category_text = []
    for x in cherche_cat:
        category_text.append(x.string.strip())
        # print(len(category_text))
        # print(f"{category_text=}")

        for catfile in category_text:
            path_cat = f"./categories/{catfile}/"
            os.makedirs(path_cat, exist_ok=True)
            # création du fichier csv d'export avec les entetes uniquement
            en_tete = [
                "product_page_url",
                "upc",
                "title",
                "price_including_tax",
                "price_excluding_tax",
                "number_available",
                "product_description",
                "category",
                "review_rating",
                "image_url",
            ]
            with open(
                f"./categories/{catfile}/{catfile}_details.csv", "w", newline=""
            ) as fichier_csv:
                obj = csv.DictWriter(fichier_csv, fieldnames=en_tete, delimiter=";")
                obj.writeheader()

    # recupération des url des catégories depuis le href
    lookfor_url_cat = []
    for y in cherche_cat:
        lookfor_url_cat.append(
            y["href"].replace("catalogue", "http://books.toscrape.com/catalogue")
        )

    # recherche du nombre de pages suivante pour chaque catégorie depuis les url
    liste_page_x_none = []
    for category_page_url in lookfor_url_cat:
        url = requests.get(category_page_url)
        page = url.content

        # transforme (parse) le HTML en objet BeautifulSoup
        soupe = bs(page, "html.parser")

        # Recherche pour une catégorie la présence de la class "current" dans la balise "li"
        # permettant de récupérer le nombre de pages
        page_next_none = soupe.find("li", class_="current")
        liste_page_x_none.append(page_next_none)

    # print(f'{liste_page_x_none=}')
    # print(len(liste_page_x_none))

    # initialisation d'un dictionnaire des catégories ayant plus d'une page
    dico_all_urls_categories = {}
    for x in range(len(liste_page_x_none)):
        dico_all_urls_categories[lookfor_url_cat[x]] = liste_page_x_none[x]

    # print(f'{dico_all_urls_categories=}')

    # reconstitution et récupération des urls des pages suivantes (page 1 sur ...) à partir du dictionnaire
    #  Ajout de ces url aux autres, celle des pages 1.
    for key, data in dico_all_urls_categories.items():
        if data is None:
            pass
        else:
            data = int(data.string.replace("Page 1 of ", "").strip())
            # print(key, " ", data)
            i = 2
            while i <= data:
                # print(key, f"page-{i}")
                lookfor_url_cat.append(key.replace("index.html", f"page-{i}.html"))
                i = i + 1

    # print(f'{lookfor_url_cat=}')
    # print(len(lookfor_url_cat))

    for book_page_scrape in lookfor_url_cat:
        scrape_books(book_page_scrape)

    # url_category = "http://books.toscrape.com/catalogue/category/books/young-adult_21/page-2.html"
    # scrape_books(url_category)


if __name__ == "__main__":
    run_scraping()
