import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Bar, Pie } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend } from 'chart.js';

// Registre os tipos de gráfico necessários
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const MoviesChart = () => {
  const [movies, setMovies] = useState([]);
  const [actorsCount, setActorsCount] = useState({});
  const [genresCount, setGenresCount] = useState({});

  useEffect(() => {
    axios.get('http://localhost:3004/unified')
      .then(response => {
        const filteredMovies = filterMovies(response.data);
        setMovies(filteredMovies);
        countActors(filteredMovies);
        countGenres(filteredMovies);
      })
      .catch(error => {
        console.error('There was an error fetching the movies!', error);
      });
  }, []);

  // Função para filtrar filmes com avaliações e tempo válidos
  const filterMovies = (movies) => {
    return movies.filter((movie) => {
      const imdbValid = movie.IMDB_score && !isNaN(parseFloat(movie.IMDB_score));
  
      if (movie.Tomatometer) {
        movie.Tomatometer = movie.Tomatometer.replace("%", "");
      }
      if (movie.Popcornmeter) {
        movie.Popcornmeter = movie.Popcornmeter.replace("%", "");
      }
  
      const tomatometerValid = movie.Tomatometer && !isNaN(parseFloat(movie.Tomatometer));
      const popcornmeterValid = movie.Popcornmeter && !isNaN(parseFloat(movie.Popcornmeter));
      const runtimeValid = movie.Runtime && parseRuntime(movie.Runtime) > 0;
  
      return imdbValid && tomatometerValid && popcornmeterValid && runtimeValid;
    });
  };
  
  // Função para contar a Frequência de aparição nos filmes
  const countActors = (movies) => {
    const actorCount = {};
    movies.forEach((movie) => {
      movie.Actors.forEach((actor) => {
        // Remova o conteúdo entre parênteses, se existir
        const cleanActorName = actor.replace(/\s*\(.*?\)\s*/g, '').trim();
  
        if (actorCount[cleanActorName]) {
          actorCount[cleanActorName]++;
        } else {
          actorCount[cleanActorName] = 1;
        }
      });
    });
    setActorsCount(actorCount);
  };
  
  // Função para contar a Frequência de aparição nos filmes
  const countGenres = (movies) => {
    const genreCount = {};
    movies.forEach((movie) => {
      movie.Genres.forEach((genre) => {
        if (genreCount[genre]) {
          genreCount[genre]++;
        } else {
          genreCount[genre] = 1;
        }
      });
    });
    setGenresCount(genreCount);
  };

  // Função para calcular a média das avaliações
  const calculateAverageRating = (movie) => {
    const imdb = parseFloat(movie.IMDB_score) * 10;
    const tomatometer = parseFloat(movie.Tomatometer);
    const popcornmeter = parseFloat(movie.Popcornmeter);

    return (imdb + tomatometer + popcornmeter) / 3;
  };


  // Função para classificar os filmes mais bem avaliados
  const topRatedMovies = () => {
    return movies
      .map((movie) => ({
        ...movie,
        averageRating: calculateAverageRating(movie),
      }))
      .sort((a, b) => b.averageRating - a.averageRating)
      .slice(0, 10);
  };

  // Função para gerar gráfico de barras para o top 10 atores mais populares
  const generateActorsChartData = () => {
    const sortedActors = Object.entries(actorsCount).sort((a, b) => b[1] - a[1]).slice(0, 10);
    return {
      labels: sortedActors.map(([actor]) => actor),
      datasets: [
        {
          label: 'Frequência de aparição nos filmes',
          data: sortedActors.map(([, count]) => count),
          backgroundColor: 'rgba(75, 192, 192, 0.5)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
        },
      ],
    };
  };

  // Função para gerar gráfico de barras para o top 10 gêneros mais populares
  const generateGenresChartData = () => {
    const sortedGenres = Object.entries(genresCount).sort((a, b) => b[1] - a[1]).slice(0, 10);
    return {
      labels: sortedGenres.map(([genre]) => genre),
      datasets: [
        {
          label: 'Frequência de aparição nos filmes',
          data: sortedGenres.map(([, count]) => count),
          backgroundColor: 'rgba(153, 102, 255, 0.5)',
          borderColor: 'rgba(153, 102, 255, 1)',
          borderWidth: 1,
        },
      ],
    };
  };

  // Função para gerar gráfico de pizza para filmes com mais ou menos de 2h
  const generateDurationPieChartData = () => {
    const durationCount = { 'Mais de 2h': 0, 'Menos de 2h': 0 };
    movies.forEach((movie) => {
      const duration = parseRuntime(movie.Runtime);
      if (duration > 120) durationCount['Mais de 2h']++;
      else durationCount['Menos de 2h']++;
    });

    return {
      labels: ['Mais de 2h', 'Menos de 2h'],
      datasets: [
        {
          label: 'Duração dos Filmes',
          data: [durationCount['Mais de 2h'], durationCount['Menos de 2h']],
          backgroundColor: ['rgba(75, 192, 192, 0.7)', 'rgba(255, 159, 64, 0.7)'],
        },
      ],
    };
  };

  const generateComparisonChartData = () => {
    const topMovies = topRatedMovies().slice(0, 5);
    return {
      labels: topMovies.map((movie) => movie.Title),
      datasets: [
        {
          label: 'IMDB (em %)',
          data: topMovies.map((movie) => parseFloat(movie.IMDB_score) * 10), // Ajustado para escala %
          backgroundColor: 'rgba(75, 192, 192, 0.7)',
        },
        {
          label: 'Tomatometer (%)',
          data: topMovies.map((movie) => parseFloat(movie.Tomatometer)),
          backgroundColor: 'rgba(153, 102, 255, 0.7)',
        },
        {
          label: 'Popcornmeter (%)',
          data: topMovies.map((movie) => parseFloat(movie.Popcornmeter)),
          backgroundColor: 'rgba(255, 159, 64, 0.7)',
        },
      ],
    };
  };
  
  
  

  // Função para converter a string de tempo para minutos
  const parseRuntime = (runtime) => {
    const match = runtime.match(/(\d+)h (\d+)m/);
    if (match) {
      return parseInt(match[1]) * 60 + parseInt(match[2]);
    } else {
      return 0;  // Caso o formato seja inválido
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '20px' }}>Dashboard de Comparação de Filmes</h1>
  
      {/* Container principal */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '20px', justifyContent: 'center' }}>
        {/* Gráfico de Barras Top 10 Atores Mais Populares */}
        <div style={{ flex: '1 1 45%', minWidth: '300px', border: '1px solid #ccc', borderRadius: '8px', padding: '20px' }}>
          <h3 style={{ textAlign: 'center' }}>Top 10 Atores Mais Populares</h3>
          <Bar data={generateActorsChartData()} />
        </div>
  
        {/* Gráfico de Barras Top 10 Gêneros Mais Populares */}
        <div style={{ flex: '1 1 45%', minWidth: '300px', border: '1px solid #ccc', borderRadius: '8px', padding: '20px' }}>
          <h3 style={{ textAlign: 'center' }}>Top 10 Gêneros Mais Populares</h3>
          <Bar data={generateGenresChartData()} />
        </div>
  
        {/* Gráfico de Pizza Filmes com Mais de 2h vs Menos de 2h */}
        <div style={{ flex: '1 1 45%', minWidth: '300px', border: '1px solid #ccc', borderRadius: '8px', padding: '20px' }}>
          <h3 style={{ textAlign: 'center' }}>Porcentagem de Filmes com Mais de 2h vs Menos de 2h</h3>
          <Pie data={generateDurationPieChartData()} />
        </div>
  
        {/* Gráfico de Comparação das Avaliações */}
        <div style={{ flex: '1 1 45%', minWidth: '300px', border: '1px solid #ccc', borderRadius: '8px', padding: '20px' }}>
          <h3 style={{ textAlign: 'center' }}>Comparação das Avaliações - Top 5 Filmes</h3>
          <Bar data={generateComparisonChartData()} />
        </div>
      </div>
  
      {/* Tabela Comparativa dos Filmes Mais Bem Avaliados */}
      <div style={{ marginTop: '30px', border: '1px solid #ccc', borderRadius: '8px', padding: '20px' }}>
        <h3 style={{ textAlign: 'center' }}>Top 10 Filmes Mais Bem Avaliados</h3>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ backgroundColor: '#f4f4f4' }}>
              <th style={{ padding: '10px', border: '1px solid #ddd' }}>Título</th>
              <th style={{ padding: '10px', border: '1px solid #ddd' }}>IMDB Score</th>
              <th style={{ padding: '10px', border: '1px solid #ddd' }}>Tomatometer</th>
              <th style={{ padding: '10px', border: '1px solid #ddd' }}>Popcornmeter</th>
              <th style={{ padding: '10px', border: '1px solid #ddd' }}>Média</th>
            </tr>
          </thead>
          <tbody>
            {topRatedMovies().map((movie, index) => (
              <tr key={index} style={{ textAlign: 'center' }}>
                <td style={{ padding: '10px', border: '1px solid #ddd' }}>{movie.Title}</td>
                <td style={{ padding: '10px', border: '1px solid #ddd' }}>{movie.IMDB_score * 10}%</td>
                <td style={{ padding: '10px', border: '1px solid #ddd' }}>{movie.Tomatometer}%</td>
                <td style={{ padding: '10px', border: '1px solid #ddd' }}>{movie.Popcornmeter}%</td>
                <td style={{ padding: '10px', border: '1px solid #ddd' }}>{movie.averageRating.toFixed(2)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}  
export default MoviesChart;
