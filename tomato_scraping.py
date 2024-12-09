"""
Módulo para extrair dados dos top 500 filmes do tomatoes para assistir em casa utilizando Selenium e BeautifulSoup.
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
driver.get("https://www.rottentomatoes.com")
# Esperando a página carregar, como não se espera um elemento específico, pode-se usar um tempo fixo em vez de usar o WebDriverWait
time.sleep(2)

# Definindo cookies para o funcionamento esperado
cookie = {
    "name": "lc-main",
    "value": "en_US",
    "domain": ".rottentomatoes.com",
    "path": "/",
    "secure": False,
    "httpOnly": False,
}
driver.add_cookie(cookie)
# Link para a página com a lista de filmes
driver.get("https://www.rottentomatoes.com/browse/movies_at_home/sort:popular?page=5")


try:
    while True:
        # Como a página carrega através de JavaScript, utiliza-se o Selenium para clicar no botão de "Load more" para carregar mais filmes.
        # Espera o elemento ser clicável e então clica o botão load more.
        wait = WebDriverWait(driver, 10)
        clickable_element = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@data-qa="dlp-load-more-button"]')
            )
        )
        driver.execute_script("arguments[0].click();", clickable_element)
        movies_list = driver.find_element(By.CLASS_NAME, "discovery-tiles__wrap")
        child_elements = movies_list.find_elements(By.XPATH, "./*")
        if len(child_elements) >= 500:
            break

finally:
    # Após cliar 9 vezes o botão de "See more", a página terá carregado 500 filmes em seu conteúdo html.
    html_page_with_500_movies = driver.find_element(By.TAG_NAME, "html").get_attribute(
        "innerHTML"
    )
    driver.quit()


# Verifica se a requisição foi bem-sucedida
if html_page_with_500_movies:
    # Criando um objeto BeautifulSoup
    tomato_soup = BeautifulSoup(html_page_with_500_movies, "html.parser")

    # Encontrando a tabela de filmes
    lista = tomato_soup.find("div", class_="discovery-tiles__wrap")
    # Extraindo os filmes
    movie_links = []
    for item in lista.find_all("div"):  # Ignorando o cabeçalho
        if item.a is None:
            continue
        movie_path = item.a["href"]
        movie_link = "https://www.rottentomatoes.com" + movie_path
        if movie_link not in movie_links:
            movie_links.append(movie_link)

    movies_data = []
    for movie_link in movie_links:
        # Definindo um cabeçalho para simular um navegador
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        try:
            # Abre-se cada título extraído da lista para obter seus dados
            movie_response = requests.get(movie_link, headers=headers, timeout=10)
        except requests.exceptions.RequestException as e:
            # Já aconteceu de levantar uma exceção devido a um timeout, então é melhor tratar.
            movie_response = None
            continue

        if movie_response and movie_response.status_code == 200:
            tomato_movie_soup = BeautifulSoup(movie_response.text, "html.parser")

            # Aqui se tem o título do filme
            media_hero = tomato_movie_soup.find("media-hero")
            media_hero_rts = media_hero.find_all("rt-text")
            movie_title = ""
            for rt in media_hero_rts:
                if "title" == rt.get("slot"):
                    movie_title = rt.get_text()

            # Procura pela div com todas as informações do filme, como gênero, data de lançamento, duração, rating, etc.
            category_wrap_divs = tomato_movie_soup.find_all(
                "div", class_="category-wrap"
            )

            genre_list = []
            release_dates = []
            runtime = ""
            rating = ""
            for div in category_wrap_divs:
                div_dt = div.find("dt").get_text()
                if "Genre" in div_dt:
                    dd = div.find("dd")
                    rt_tags = dd.find_all("rt-link")
                    for div in rt_tags:
                        genre_list.append(div.get_text())

                elif "Release Date (Theaters)" in div_dt:
                    dd = div.find("dd")
                    release_dates.append("Theaters: " + dd.find("rt-text").get_text())

                elif "Release Date (Streaming)" in div_dt:
                    dd = div.find("dd")
                    release_dates.append("Streaming: " + dd.find("rt-text").get_text())

                elif "Runtime" in div_dt:
                    dd = div.find("dd")
                    runtime = dd.find("rt-text").get_text()

                elif "Rating" in div_dt:
                    dd = div.find("dd")
                    rating = dd.find("rt-text").get_text()

            actor_list = []
            actor_section = tomato_movie_soup.find("section", class_="cast-and-crew")
            if actor_section:
                actor_wrap = actor_section.find("div", class_="content-wrap")
                actors_anchors = actor_wrap.find_all("a", {"data-qa": "person-item"})
                for actor_anchor in actors_anchors:
                    text_divs = actor_anchor.find("div", {"slot": "insetText"})
                    actor = text_divs.find("p", class_="name")
                    character = text_divs.find("p", class_="role")
                    actor_list.append(f"{actor.get_text()} ({character.get_text()})")

            tomatometer = tomato_movie_soup.find(
                "rt-text", {"slot": "criticsScore"}
            ).get_text()
            popcornmeter = tomato_movie_soup.find(
                "rt-text", {"slot": "audienceScore"}
            ).get_text()

            movie_data = {
                "Title": movie_title,
                "Genres": genre_list,
                "Release Dates": release_dates,
                "Runtime": runtime,
                "Rating": rating,
                "Actors": actor_list,
                "Tomatometer": tomatometer,
                "Popcornmeter": popcornmeter,
            }

            movies_data.append(movie_data)
            print(len(movies_data))

            with open("./movies_data/tomato.json", "w", encoding="utf-8") as file:
                json.dump(movies_data, file, ensure_ascii=False, indent=4)
