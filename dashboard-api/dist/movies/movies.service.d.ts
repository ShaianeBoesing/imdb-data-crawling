export declare class MoviesService {
    private readonly movies;
    getMovies(): {
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
