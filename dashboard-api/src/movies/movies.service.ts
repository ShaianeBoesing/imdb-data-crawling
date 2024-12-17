import { Injectable } from '@nestjs/common';

@Injectable()
export class MoviesService {
  private readonly movies = [
    {
      Title: 'Gladiator',
      'Theaters release Date': '2000',
      'Streaming release Date': '2011',
      Runtime: '2h 35m',
      age_rating: 'R',
      Genres: [
        'Adventure Epic',
        'Sword & Sandal',
        'Action',
        'Action Epic',
        'Adventure',
        'Period Drama',
        'Epic',
        'History',
        'Drama',
      ],
      Actors: [
        'Djimon Hounsou (Juba)',
        'John Shrapnel (Gaius)',
        'Ralf Moeller (Hagen)',
        'Connie Nielsen (Lucilla)',
        'David Schofield (Falco)',
        'Sven-Ole Thorsen (Tiger)',
        'Nicholas McGaughey (Praetorian Officer)',
        'Tommy Flanagan (Cicero)',
        'Derek Jacobi (Gracchus)',
        'Joaquin Phoenix (Commodus)',
        'Tomas Arana (Quintus)',
        'Russell Crowe (Maximus)',
        'Russell Crowe (Maximus Decimus Meridius)',
        'Omid Djalili (Slave Trader)',
        'Oliver Reed (Proximo)',
        'Spencer Treat Clark (Lucius)',
        'David Hemmings (Cassius)',
        'Chris Kell (Scribe)',
        'Ridley Scott (Director)',
        'Richard Harris (Marcus Aurelius)',
      ],
      IMDB_score: '8.5',
      Tomatometer: '80%',
      Popcornmeter: '87%',
    },
    {
      Title: 'Deadpool & Wolverine',
      'Theaters release Date': '2024',
      'Streaming release Date': '2024',
      Runtime: '2h 8m',
      age_rating: 'R',
      Genres: [
        'Superhero',
        'Action',
        'Comedy',
        'Adventure',
        'Raunchy Comedy',
        'Buddy Comedy',
        'Sci-Fi',
        'Dark Comedy',
      ],
      Actors: [
        'Dafne Keen (Laura)',
        'Tyler Mane (Sabretooth)',
        'Chris Evans (Johnny Storm)',
        'Leslie Uggams (Blind Al)',
        'Shawn Levy (Director)',
        'Emma Corrin (Cassandra Nova)',
        'Wesley Snipes (Blade)',
        'Hugh Jackman (Logan)',
        'Jennifer Garner (Elektra)',
        'Aaron Stanford (Pyro)',
        'Ryan Reynolds (Wade Wilson)',
        'Channing Tatum (Gambit)',
        'Henry Cavill (The Cavillrine)',
        'Wunmi Mosaku (B-15)',
        'Morena Baccarin (Vanessa)',
        'Rob Delaney (Peter)',
        'Karan Soni (Dopinder)',
        'Matthew Macfadyen (Mr. Paradox)',
        'Jon Favreau (Happy Hogan)',
      ],
      IMDB_score: '7.7',
      Tomatometer: '78%',
      Popcornmeter: '94%',
    },
  ];

  getMovies() {
    return this.movies;
  }
}