import { MoviesService } from './movies.service';
export declare class MoviesController {
    private readonly moviesService;
    constructor(moviesService: MoviesService);
    findAll(): {
        Title: string;
        'Theaters release Date': string;
        'Streaming release Date': string;
        Runtime: string;
        age_rating: string;
        Genres: string[];
        Actors: string[];
        IMDB_score: string;
        Tomatometer: string;
        Popcornmeter: string;
    }[];
}
