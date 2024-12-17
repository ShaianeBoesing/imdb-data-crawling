"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.MoviesService = void 0;
const common_1 = require("@nestjs/common");
let MoviesService = class MoviesService {
    constructor() {
        this.movies = [
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
    }
    getMovies() {
        return this.movies;
    }
};
exports.MoviesService = MoviesService;
exports.MoviesService = MoviesService = __decorate([
    (0, common_1.Injectable)()
], MoviesService);
//# sourceMappingURL=movies.service.js.map