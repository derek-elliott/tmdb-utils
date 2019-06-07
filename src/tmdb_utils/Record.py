import datetime
from typing import List, Any

from . import DataClasses as dc
from . import Database as db
from dateutil import parser


class Record:
    """Represents a complete record of TMDB movie"""
    def __init__(self, id: int, budget: int, homepage: str, imdb_id: str, original_language: str, original_title: str,
                 overview: str, popularity: float, poster_path: str, release_date: datetime.date, runtime: int,
                 status: str, tagline: str, title: str, revenue: int, collection: dc.Collection,
                 production_companies: List[dc.ProductionCompany], production_countries: List[dc.Country],
                 keywords: List[dc.Keyword], cast: List[dc.Cast], crew: List[dc.Crew],
                 spoken_languages: List[dc.Language], genres: List[dc.Genre], table_name: str = 'tmdb_movies'):
        self.id = id  #: TMDB ID
        self.budget = budget #: Movie budget
        self.homepage = homepage  #: Link to movie homepage
        self.imdb_id = imdb_id  #: Movie id on IMDB
        self.original_language = original_language
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
        self.collection = collection  #: Object of the collection the movie belongs to, if any
        self.production_companies = production_companies  #: List of production company ids involved with the movie
        self.production_countries = production_countries  #: List of countries that the movie was produced in
        self.keywords = keywords  #: List of ids of keywords describing the movie
        self.cast = cast  #: List of the cast ids involved with the movie
        self.crew = crew  #: List of the crew ids involved with the movie
        self.spoken_languages = spoken_languages  #: List of language ids spoken in the movie
        self.genres = genres  #: List of genre ids related to the movie
        self.table_name = table_name  #: Default name of the Postgres table to store Movie in

    @staticmethod
    def from_dict(raw_record: dict):
        """Creates a new Record from a dictionary

        Args:
             raw_record: The raw record in a dictionary, usually from parsing with the csv library

        Returns:
             A Record object
        """
        basic_keys = ['id', 'budget', 'homepage', 'imdb_id', 'original_language', 'original_title', 'overview', 'popularity', 'poster_path',
                      'runtime', 'status', 'tagline', 'title', 'revenue', ]
        unchanged_items = {key: value for key, value in raw_record.items() if key in basic_keys}
        release_date = parser.parse(raw_record['release_date'], fuzzy_with_tokens=True)[0].date()

        genres = [dc.Genre(**genre) for genre in raw_record['genres']]
        collection = [dc.Collection(**collection) for collection in raw_record['belongs_to_collection']][0]
        companies = [dc.ProductionCompany(**company) for company in raw_record['production_companies']]
        keywords = [dc.Keyword(**keyword) for keyword in raw_record['keywords']]
        cast = [dc.Cast(movie_id=raw_record['id'], **person) for person in raw_record['cast']]
        crew = [dc.Crew(movie_id=raw_record['id'], **person) for person in raw_record['crew']]
        spoken_languages = [dc.Language(**language) for language in raw_record['spoken_languages']]
        countries = [dc.Country(**country) for country in raw_record['production_countries']]

        return Record(release_date=release_date, genres=genres, collection=collection, production_companies=companies,
                      keywords=keywords, cast=cast, crew=crew, spoken_languages=spoken_languages,
                      production_countries=countries, **unchanged_items)

    def get_movie_insert_statement(self) -> str:
        """Generates an insert statement for the Movie table

        Returns:
            Movie insert string
        """
        genre_ids = ' ,'.join([str(genre.id) for genre in self.genres])
        production_company_ids = ', '.join([str(company.id) for company in self.production_companies])
        production_country_ids = ', '.join([str(country.id) for country in self.production_countries if country.id is not ''])
        spoken_language_ids = ', '.join([str(language.id) for language in self.spoken_languages if language.id is not ''])
        keyword_ids = ', '.join([str(keyword.id) for keyword in self.keywords])

        return (f"INSERT INTO {self.table_name} VALUES({self.id}, "
                f"{self.collection.id}, "
                f"{self.budget}, "
                f"ARRAY [{genre_ids}], "
                f"$${self.homepage}$$, "
                f"$${self.imdb_id}$$, "
                f"{self.original_language}, "
                f"$${self.original_title}$$, "
                f"$${self.overview}$$, "
                f"{self.popularity}, "
                f"$${self.poster_path}$$, "
                f"ARRAY [{production_company_ids}], "
                f"ARRAY [{production_country_ids}], "
                f"{self.release_date}, "
                f"{self.runtime}, "
                f"ARRAY [{spoken_language_ids}], "
                f"$${self.status}$$, "
                f"$${self.tagline}$$, "
                f"$${self.title}$$, "
                f"ARRAY [{keyword_ids}], "
                f"{self.revenue}) ON CONFLICT (id) DO NOTHING")

    def write_to_postgres(self, database: db.Database):
        """Writes the Movie to Postgres

        Args:
            database: Database object to write to

        Returns:

        """
        for language in self.spoken_languages:
            language.id = self.get_id(language, database)
        for country in self.production_countries:
            country.id = self.get_id(country, database)

        if not database.execute_insert(self.get_movie_insert_statement()):
            print(f'Failed to write Movie: {self.title} to Postgres')
        if database.execute_insert(self.collection.get_insert_statement()):
            pass
        else:
            print(f'Failed to write Collection: {self.collection.name}')
        for genre in self.genres:
            if not database.execute_insert(genre.get_insert_statement()):
                print(f'Failed to write Genre: {genre.name}')
        for company in self.production_companies:
            if not database.execute_insert(company.get_insert_statement()):
                print(f'Failed to write Company: {company.name}')
        for keyword in self.keywords:
            if not database.execute_insert(keyword.get_insert_statement()):
                print(f'Failed to write Keyword: {keyword.name}')
        for person in self.cast:
            if not database.execute_insert(person.get_insert_statement()):
                print(f'Failed to write Cast: {person.name}')
        for person in self.crew:
            if not database.execute_insert(person.get_insert_statement()):
                print(f'Failed to write Crew: {person.name}')
        print(f'Successfully wrote Movie: {self.title} and related objects to Postgres')

    @staticmethod
    def get_id(obj: Any, database: db.Database) -> int:
        """Gets the id of an object.  If the object doesn't exist in the database, will write it and return the new id

        Args:
            obj: Object to ge the id for
            database: Database object to write to

        Returns:
            The id as an integer
        """
        orig_id = database.execute_query_for_one(obj.get_id_query_statement())

        if orig_id is None:
            database.execute_insert(obj.get_insert_statement())
            return database.execute_query_for_one(obj.get_id_query_statement())
        else:
            return orig_id

