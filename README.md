# Executando as Aplicações

## Apresentação do trabalho
https://youtu.be/AVW1AjT4r2Y

## Pré-requisitos

Antes de iniciar, certifique-se de ter instalado as seguintes ferramentas em sua máquina:

- **Node.js**: `v20` (ou superior)
- **npm**: `v10` (ou superior)
- **python**: `v3` 

## Passo-a-passo

### Crawler
- Acesse o diretório `crawler`
- Caso deseje realizar a extração de dados novamente, você deve executar:
- Lembre-se que dados extraídos já estão disponíveis e sendo consumidos pela API. Portanto, se o seu objetivo for apenas visualizar o dashboard com esses dados, não é necessário executar o crawler novamente.
```
  pip install -r requirements.txt
  python3 imdb_scraping.py
  python3 tomato_scraping.py
  python3 json_unifier.py
```

### API
- Acesse o diretório `dashboard-api`
```
  npm install
  npm run start:dev
```

### Front-end
- Acesse o diretório `dashboard-frontend`
```
  npm install
  npm start
```
