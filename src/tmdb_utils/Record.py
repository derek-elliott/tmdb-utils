import DataClasses as dc
from typing import List
import datetime
from dateutil import parser

class Record:
    """Represents a complete record of TMDB movie"""
    def __init__(self, id: int, budget: int, homepage: str, imdb_id: str, original_title: str, overview: str,
                 popularity: float, poster_path: str, release_date: datetime.date, runtime: int, status: str,
                 tagline: str, title: str, revenue: int, collection: dc.Collection, original_language: dc.Language,
                 production_companies: List[dc.ProductionCompany], production_countries: List[dc.ProductionCountry],
                 keywords: List[dc.Keyword], cast: List[dc.Cast], crew: List[dc.Crew],
                 spoken_languages: List[dc.Language], genres: List[dc.Genre], table_name: str):
        self.id = id  #: TMDB ID
        self.budget = budget #: Movie budget
        self.homepage = homepage  #: Link to movie homepage
        self.imdb_id = imdb_id  #: Movie id on IMDB
        self.original_title = original_title  #: Original title of the Movie
        self.overview = overview  #: Overview of the movie
        self.popularity = popularity  #: Popularity of movie out of 100
        self.poster_path = poster_path  #: Link to movie poster
        self.release_date = release_date  #: Release date of the movie
        self.runtime = runtime  #: Runtime of the movie
        self.status = status  #: Release status of the movie
        self.tagline = tagline  #: Movie tagline
        self.title = title  #: Movie title
        self.revenue = revenue  #: Revenue of the movie
        self.collection = collection  #: Id of the collection the movie belongs to, if any
        self.original_language = original_language  #: The original language of the movie
        self.production_companies = production_companies  #: List of production company ids involved with the movie
        self.production_countries = production_countries  #: List of countries that the movie was produced in
        self.keywords = keywords  #: List of ids of keywords describing the movie
        self.cast = cast  #: List of the cast ids involved with the movie
        self.crew = crew  #: List of the crew ids involved with the movie
        self.spoken_languages = spoken_languages  #: List of language ids spoken in the movie
        self.genres = genres  #: List of genre ids related to the movie
        self.table_name = table_name  #: Default name of the Postgres table to store Movie in

    @staticmethod
    def from_dict(raw_record: dict) -> Record:
        """Creates a new Record from a dictionary

        Args:
             raw_record: The raw record in a dictionary, usually from parsing with the csv library

        Returns:
             A Record object
        """
        basic_keys = ['id', 'budget', 'homepage', 'imdb_id', 'original_title', 'overview', 'popularity', 'poster_path',
                      'runtime', 'status', 'tagline', 'title', 'revenue']
        unchanged_items = {key: value for key, value in raw_record.items() if key in basic_keys}
        release_date = parser.parse(raw_record['release_date'], fuzzy_with_tokens=True)[0].date()

        genres = [dc.Genre(**genre) for genre in raw_record['genres']]
        collection = [dc.Collection(**collection) for collection in raw_record['belongs_to_collection']]
        companies = [dc.ProductionCompany(**company) for company in raw_record['production_companies']]
        keywords = [dc.Keyword(**keyword) for keyword in raw_record['keywords']]
        cast = [dc.Cast(**person) for person in raw_record['cast']]
        crew = [dc.Crew(**person) for person in raw_record['crew']]
        spoken_languages = [dc.Language(**language) for language in raw_record['spoken_languages']]
        countries = [dc.ProductionCountry(**country) for country in raw_record['production_countries']]

        return Record(release_date=release_date, genres=genres, collection=collection, production_companies=companies,
                      keywords=keywords, cast=cast, crew=crew, spoken_languages=spoken_languages,

                      production_countries=countries, **unchanged_items)


    def get_movie_insert_statement(self) -> str:
        """Generates an insert statement for the Movie table

        Returns:
            Movie insert string
        """
        return (f"INSERT INTO {self.table_name} VALUES({self.id}, "
                f"{self.collection_id}, "
                f"{self.budget}, "
                f"{self.genre_ids}, "
                f"$${self.homepage}$$, "
                f"{self.imdb_id}, "
                f"{self.original_language_id}, "
                f"$${self.original_title}$$, "
                f"$${self.overview}$$, "
                f"{self.popularity}, "
                f"$${self.poster_path}$$, "
                f"{self.production_company_ids}, "
                f"{self.production_country_ids}, "
                f"{self.release_date}, "
                f"{self.runtime}, "
                f"{self.spoken_language_ids}, "
                f"$${self.status}$$, "
                f"$${self.tagline}$$, "
                f"$${self.title}$$, "
                f"{self.keyword_ids}, "
                f"{self.cast_ids}, "
                f"{self.crew_ids}, "
                f"{self.revenue}) ON CONFLICT (id) DO NOTHING")

    def write_to_postgres(self):
        
