import requests
from bs4 import BeautifulSoup

# URL do IMDb que você deseja fazer o scraping
url = 'https://www.imdb.com/chart/top'

# Definindo um cabeçalho para simular um navegador
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Fazendo uma requisição GET para a página com o cabeçalho
response = requests.get(url, headers=headers, timeout=10)
# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    # Criando um objeto BeautifulSoup
    imdb_soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrando a tabela de filmes
    lista = imdb_soup.find('ul', class_='ipc-metadata-list')
    # Extraindo os filmes
    movies = []
    for item in lista.find_all('li'):  # Ignorando o cabeçalho
        title_container = item.find('div', class_='ipc-title')
        metadata_container = item.find('div', class_='cli-title-metadata').find_all('span')
        rating_container = item.find('div', class_='cli-ratings-container')

        movie_path = title_container.a['href']
        title = title_container.a.h3.get_text()
        year = metadata_container[0].get_text()
        duration = metadata_container[1].get_text()
        age_rating = metadata_container[2].get_text()
        rating = rating_container.span.span.get_text()

        print('Título: ', title)
        print('Ano: ', year)
        print('Duração: ', duration)
        print('Classificação etária: ', age_rating)
        print('Avaliação: ', rating)

        # Requisição para a página do filme para obter mais detalhes
        movie_link = "https://www.imdb.com" + movie_path
        movie_response = requests.get(movie_link, headers=headers, timeout=10)
        
        if movie_response.status_code == 200:
            imdb_movie_soup = BeautifulSoup(movie_response.text, 'html.parser')

            # Extraindo mais dados da página do filme
            gender_list = imdb_movie_soup.find('div', class_="ipc-chip-list__scroller")
            gender_list_name = []
            for gender in gender_list.find_all('a'):
                gender_name = gender.get_text()
                gender_list_name.append(gender_name)
            print('Gêneros: ', gender_list_name)
            
            actors_list = imdb_movie_soup.find_all('a', {"data-testid": "title-cast-item__actor"})
            actors_list_name = []
            characters_list = imdb_movie_soup.find_all('a', {"data-testid": "cast-item-characters-link"})
            for actor, characters in zip(actors_list, characters_list):
                # print(characters)
                actor_character_name = f"{actor.get_text()} ({characters.span.get_text()})"
                actors_list_name.append(actor_character_name)   
            print("Atores: ", actors_list_name)
            
        else:
            print(f'Erro ao acessar a página do filme: {movie_link}')
else:
    print(f'Erro ao acessar a página principal: {url}')
