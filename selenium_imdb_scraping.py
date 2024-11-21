from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
import requests
from bs4 import BeautifulSoup
import json
import time

# Set up the WebDriver (Chrome in this example)
chrome_options = ChromeOptions()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (Windows)
chrome_options.add_argument("--no-sandbox")  # Required for some environments

firefox_options = FirefoxOptions()
firefox_options.add_argument("--headless")  # Run Chrome in headless mode
firefox_options.headless = True
firefox_options.page_load_strategy = 'eager'

driver = webdriver.Firefox(options=firefox_options)
# cookie = {
#     'name': 'lc-main',         # Cookie name
#     'value': 'en_US',     # Cookie value
#     'domain': '.imdb.com',
#     'path': '/',  # Optional, usually set to '/'
#     'secure': False,  # Set to True if the site uses HTTPS
#     'httpOnly': False  # I      # Domain for the cookie
# }
# driver.add_cookie(cookie)

# Open the page
driver.get("https://www.imdb.com")
time.sleep(2)  # or use WebDriverWait here if you want to wait for a specific element

# Set the cookie once the page is loaded
cookie = {
    'name': 'lc-main',         # Cookie name
    'value': 'en_US',          # Cookie value
    'domain': '.imdb.com',     # Cookie domain
    'path': '/',               # Cookie path
    'secure': False,           # Set to True if the site uses HTTPS
    'httpOnly': False          # Set to True if the cookie is HttpOnly
}
driver.add_cookie(cookie)
driver.get("http://www.imdb.com/search/title/?groups=top_1000")

# Wait until a specific element is loaded (adjust this as needed)
# Here, it waits up to 10 seconds for an element with id "content" to load
try:
    for _ in range(10):
        # element = WebDriverWait(driver, 15).until(
        # EC.visibility_of_element_located((By.CSS_SELECTOR, "button.ipc-see-more__button"))
        # )

    # Then wait for the element to be clickable
        clickable_element = driver.find_element(By.CLASS_NAME, "ipc-see-more__button")
        print("found the button")
        driver.execute_script("arguments[0].click();", clickable_element)
        print("clicked")
        time.sleep(2)
        # a = WebDriverWait(driver, 15).until(
        #     EC.element_to_be_selected((By.CSS_SELECTOR, "button.ipc-see-more__button"))
        # )

        # clickable_element.click()
        # time.sleep(10)
    # print("Page fully loaded!")
    # # Optionally, you can get the page source after it's fully loaded
    # page_source = driver.page_source
    # print(page_source)
finally:
    # Close the WebDriver after the operations
    html_page_with_500_movies = driver.find_element(By.TAG_NAME, "html").get_attribute('innerHTML')
    driver.quit()
# print(html_page_with_500_movies)
imdb_soup = BeautifulSoup(html_page_with_500_movies, 'html.parser')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
    # Encontrando a tabela de filmes
lista = imdb_soup.find('ul', class_='ipc-metadata-list')
# print(lista)
# Extraindo os filmes
movies = []
for item in lista.find_all('li'):  # Ignorando o cabeçalho
    title_container = item.find('div', class_='ipc-title')
    metadata_container = item.find('div', class_='ipc-metadata-list-summary-item__tc').find_all('span')
    rating_container = item.find('span', class_='ipc-rating-star--rating')

    movie_path = title_container.a['href']
    title = title_container.a.h3.get_text()
    year = metadata_container[0].get_text()
    duration = metadata_container[1].get_text()
    age_rating = metadata_container[2].get_text()
    rating = rating_container.get_text()

    # Requisição para a página do filme para obter mais detalhes
    movie_link = "https://www.imdb.com" + movie_path
    movie_response = requests.get(movie_link, cookies={"lc-main": "en_US"}, headers=headers, timeout=10)
    
    if movie_response.status_code == 200:
        imdb_movie_soup = BeautifulSoup(movie_response.text, 'html.parser')

        # Extraindo mais dados da página do filme
        gender_list = imdb_movie_soup.find('div', class_="ipc-chip-list__scroller")
        gender_list_name = []
        for gender in gender_list.find_all('a'):
            gender_name = gender.get_text()
            gender_list_name.append(gender_name)
        
        actors_list = imdb_movie_soup.find_all('a', {"data-testid": "title-cast-item__actor"})
        actors_list_name = []
        characters_list = imdb_movie_soup.find_all('a', {"data-testid": "cast-item-characters-link"})
        for actor, characters in zip(actors_list, characters_list):
            actor_character_name = f"{actor.get_text()} ({characters.span.get_text()})"
            actors_list_name.append(actor_character_name)   
        
        # Adicionando os dados do filme ao dicionário
        movie_data = {
            'Title': title,
            'Release Dates': year,
            'Runtime': duration,
            'Rating': age_rating,
            'imdb_score': rating,
            'Genres': gender_list_name,
            'Actors': actors_list_name
        }
        movies.append(movie_data)
        print(movie_data)
    else:
        print(f'Erro ao acessar a página do filme: {movie_link}')

    # Escrevendo os dados em um arquivo JSON
    with open('./imdb_movies.json', 'w', encoding='utf-8') as json_file:
        json.dump(movies, json_file, ensure_ascii=False, indent=4)
        print(len(movies))