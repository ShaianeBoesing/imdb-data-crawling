"""
Módulo para extrair dados dos top 500 filmes do IMDb utilizando Selenium e BeautifulSoup.
Alunos:
    Matheus Eduardo Lafeta Feliciano (21202339)
    Shaiane Boesing Rodrigues Borges (21202341)
"""

import json
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Configuração do WebDriver (Firefox)
firefox_options = FirefoxOptions()
firefox_options.add_argument("--headless")
firefox_options.headless = True
firefox_options.page_load_strategy = "eager"

driver = webdriver.Firefox(options=firefox_options)


# Link base para o Selenium carregar inicialmente
driver.get("https://www.imdb.com")
# Esperando a página carregar, como não se espera um elemento específico, pode-se usar um tempo fixo em vez de usar o WebDriverWait
time.sleep(2)

# Definindo cookies para o funcionamento esperado
cookie = {
    "name": "lc-main",
    "value": "en_US",
    "domain": ".imdb.com",
    "path": "/",
    "secure": False,
    "httpOnly": False,
}
driver.add_cookie(cookie)
# Link para a página com a lista de filmes dos top 1000 filmes do IMDb
driver.get("http://www.imdb.com/search/title/?groups=top_1000")


try:
    for _ in range(9):
        # Como a página carrega através de JavaScript, utiliza-se o Selenium para clicar no botão de "See more" (Inicia-se com 50 filmes)
        # para carregar mais filmes (a cada clique se carrega  mais 50).
        wait = WebDriverWait(driver, 10)
        # Espera o elemento ser clicável e então clica o botão see more.
        clickable_element = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "ipc-see-more__button"))
        )
        driver.execute_script("arguments[0].click();", clickable_element)


finally:
    # Após cliar 9 vezes o botão de "See more", a página terá carregado 500 filmes em seu conteúdo html.
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ipc-see-more__button")))
    html_page_with_500_movies = driver.find_element(By.TAG_NAME, "html").get_attribute(
        "innerHTML"
    )
    driver.quit()

# A partir daqui utlizamos o BeautifulSoup para extrair os dados dos filmes
imdb_soup = BeautifulSoup(html_page_with_500_movies, "html.parser")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Encontrando a tabela de filmes na página com 500 filmes.
lista = imdb_soup.find("ul", class_="ipc-metadata-list")

movies = []
for index, item in enumerate(lista.find_all("li")):
    title_container = item.find("div", class_="ipc-title")
    # A partir da página inicial, é possível extrair o link para a página do filme
    movie_path = title_container.a["href"]

    # Link completo para a página do filme para obter mais detalhes
    movie_link = "https://www.imdb.com" + movie_path
    movie_response = requests.get(
        movie_link, cookies={"lc-main": "en_US"}, headers=headers, timeout=10
    )

    if movie_response.status_code == 200:
        imdb_movie_soup = BeautifulSoup(movie_response.text, "html.parser")

        title = imdb_movie_soup.find(
            "span", {"data-testid": "hero__primary-text"}
        ).get_text()

        metadata_container = imdb_movie_soup.find(
            "ul",
            class_="ipc-inline-list ipc-inline-list--show-dividers sc-ec65ba05-2 joVhBE baseAlt",
        ).find_all("li")

        year = ""
        duration = ""
        age_rating = ""

        for li in metadata_container:
            if li.a:
                if "/releaseinfo" in li.a["href"]:
                    year = li.get_text()
                if "/parentalguide/certificates" in li.a["href"]:
                    age_rating = li.get_text()
            else:
                duration = li.get_text()

        print(year, duration, age_rating)

        rating = imdb_movie_soup.find("span", class_="sc-d541859f-1 imUuxf").get_text()

        gender_list = imdb_movie_soup.find("div", class_="ipc-chip-list__scroller")
        gender_list_name = []
        for gender in gender_list.find_all("a"):
            gender_name = gender.get_text()
            gender_list_name.append(gender_name)

        actors_list = imdb_movie_soup.find_all(
            "a", {"data-testid": "title-cast-item__actor"}
        )
        actors_list_name = []
        characters_list = imdb_movie_soup.find_all(
            "a", {"data-testid": "cast-item-characters-link"}
        )
        for actor, characters in zip(actors_list, characters_list):
            actor_character_name = f"{actor.get_text()} ({characters.span.get_text()})"
            actors_list_name.append(actor_character_name)

        # Adicionando os dados do filme ao dicionário
        movie_data = {
            "Title": title,
            "Release Dates": year,
            "Runtime": duration,
            "Rating": age_rating,
            "imdb_score": rating,
            "Genres": gender_list_name,
            "Actors": actors_list_name,
        }

        movies.append(movie_data)

    else:
        print(f"Erro ao acessar a página do filme: {movie_link}")

    # Escrevendo os dados em um arquivo JSON
    with open("./movies_data/imdb.json", "w", encoding="utf-8") as json_file:
        json.dump(movies, json_file, ensure_ascii=False, indent=4)
        print(len(movies))
