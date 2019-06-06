"""Dataclasses for elements of a TMDB record

Defines objects for parts of a TMDB record and provides insert statements for Postgres

"""
from dataclasses import dataclass, field
from typing import List
import datetime


@dataclass
class Movie:
    """An object representing one Movie in the TMDB dataset"""
    id: int  #: TMDB ID
    budget: int  #: Movie budget
    homepage: str  #: Link to movie homepage
    imdb_id: str  #: Movie id on IMDB
    original_title: str  #: Original title of the Movie
    overview: str  #: Overview of the movie
    popularity: float  #: Popularity of movie out of 100
    poster_path: str  #: Link to movie poster
    release_date: datetime.date  #: Release date of the movie
    runtime: int  #: Runtime of the movie
    status: str  #: Release status of the movie
    tagline: str  #: Movie tagline
    title: str  #: Movie title
    revenue: int  #: Revenue of the movie
    collection_id: int = -1  #: Id of the collection the movie belongs to, if any
    original_language_id: int = -1  #: The original language of the movie
    production_company_ids: List[int] = field(default_factory=list)  #: List of production company ids involved with the movie
    production_country_ids: List[int] = field(default_factory=list)  #: List of countries that the movie was produced in
    keyword_ids: List[int] = field(default_factory=list)  #: List of ids of keywords describing the movie
    cast_ids: List[int] = field(default_factory=list)  #: List of the cast ids involved with the movie
    crew_ids: List[int] = field(default_factory=list)  #: List of the crew ids involved with the movie
    spoken_language_ids: List[int] = field(default_factory=list)  #: List of language ids spoken in the movie
    genre_ids: List[int] = field(default_factory=list)  #: List of genre ids related to the movie
    table_name: str = 'tmdb_movies'  #: Default name of the Postgres table to store Movie in

    def get_insert_statement(self) -> str:
        """Generates an insert statement for the Movie object

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


@dataclass
class Collection:
    id: int  #: Collection id
    name: str  #: Collection name
    poster_path: str  #: Link to collection poster
    backdrop_path: str  #: Link to collection backdrop path
    table_name: str = 'tmdb_collection'  #: Default name of Postgres table to store Collection in

    def get_insert_statement(self) -> str:
        """Generates an insert statement for the Collection object

        Returns:
            Collection insert string
        """
        return (f"INSERT INTO {self.table_name} VALUES({self.id}, "
                f"$${self.name}$$, "
                f"$${self.poster_path}$$, "
                f"$${self.backdrop_path}$$) ON CONFLICT (id) DO NOTHING")


@dataclass
class Genre:
    id: int  #: Genre id
    name: str  #: Genre name
    table_name: str = 'tmdb_genres'  #: Default name of Postgres table to store Genre in

    def get_insert_statement(self) -> str:
        """Generates an insert statement for the Genre object

            Returns:
                Genre insert string
            """
        return (f"INSERT INTO {self.table_name} VALUES({self.id}, "
                f"$${self.name}$$) ON CONFLICT (id) DO NOTHING")


@dataclass
class ProductionCompany:
    id: int  #: ProductionCompany id
    name: str  #: ProductionCompany name
    table_name: str = 'tmdb_production_companies'  #: Default name of Postgres table to store ProductionCompany in

    def get_insert_statement(self) -> str:
        """Generates an insert statement for the ProductionCompany object

        Returns:
            ProductionCompany insert string
        """
        return (f"INSERT INTO {self.table_name} VALUES({self.id}, "
                f"$${self.name}$$) ON CONFLICT (id) DO NOTHING")


@dataclass
class Country:
    iso_3166_1: str  #: Country iso 3166-1 code
    name: str  #: Name of Country
    table_name: str = 'tmdb_countries'  #: Default name of Postgres table to store Country in
    id: int = None  #: Country id

    def get_insert_statement(self) -> str:
        """Generates an insert statement for the Country object

        Returns:
            Country insert string
        """
        if self.id is None:
            return (f"INSERT INTO {self.table_name}(iso_3166_1, name) VALUES($${self.iso_3166_1}$$, "
                    f"$${self.name}$$) ON CONFLICT (id) DO NOTHING")
        else:
            return (f"INSERT INTO {self.table_name} VALUES({self.id}, "
                    f"$${self.iso_3166_1}$$, "
                    f"$${self.name}$$) ON CONFLICT (id) DO NOTHING")


@dataclass
class Language:
    iso_639_1: str  #: Language iso 639-1 code
    name: str  #: Name of Language
    table_name: str = 'tmdb_languages'  #: Default name of Postgres table to store Language in
    id: int = None  #: Language id

    def get_insert_statement(self) -> str:
        """Generates an insert statement for the Language object

        Returns:
            Language insert string
        """
        if self.id is None:
            return (f"INSERT INTO {self.table_name}(iso_639_1, name) VALUES($${self.iso_639_1}$$, "
                    f"$${self.name}$$) ON CONFLICT (id) DO NOTHING")
        else:
            return (f"INSERT INTO {self.table_name} VALUES({self.id}, "
                    f"$${self.iso_639_1}$$, "
                    f"$${self.name}$$) ON CONFLICT (id) DO NOTHING")


@dataclass
class Keyword:
    id: int  #: Keyword id
    name: str  #: Keyword
    table_name: str = 'tmdb_keywords'  #: Default name of Postgres table to store Keyword in

    def get_insert_statement(self) -> str:
        """Generates an insert statement for the Keyword object

        Returns:
            Keyword insert string
        """
        return (f"INSERT INTO {self.table_name} VALUES({self.id}, "
                f"$${self.name}$$) ON CONFLICT (id) DO NOTHING")


@dataclass
class Cast:
    id: int  #: Cast id
    movie_id: int  #: Related Movie id
    cast_id: int  #: TMDB cast id
    credit_id: str  #: TMDB credit id
    character: str  #: Character name
    gender: int  #: Gender code
    name: str  #: Name of cast member
    order: int  #: Order appearing in credits
    profile_path: str  #: Path to TMDB profile
    table_name: str = 'tmdb_cast'  #: Default name of Postgres table to store Cast in

    def get_insert_statement(self) -> str:
        """Generates an insert statement for the Cast object

        Returns:
            Cast insert string
        """
        return (f"INSERT INTO {self.table_name} VALUES({self.id}, "
                f"{self.movie_id}, "
                f"{self.cast_id}, "
                f"$${self.credit_id}$$, "
                f"ARRAY[$${'$$, '.join(self.character.split('/'))}$$], "
                f"$${self.gender}$$, "
                f"$${self.name}$$, "
                f"{self.order}, "
                f"$${self.profile_path}$$) ON CONFLICT (id) DO NOTHING")


@dataclass
class Crew:
    id: int  #: Crew id
    movie_id: int  #: Related Movie id
    credit_id: str  #: TMDB credit id
    department: str  #: Department crew member worked in
    gender: int  #: Gender code
    job: str  #: Job crew member performed
    name: str  #: Name of crew member
    profile_path: str  #: Path to TMDB profile
    table_name: str = 'tmdb_crew'  #: Default name of Postgres table to store Crew in

    def get_insert_statement(self) -> str:
        """Generates an insert statement for the Crew object

        Returns:
            Crew insert string
        """
        return (f"INSERT INTO {self.table_name} VALUES({self.id}, "
                f"{self.movie_id}, "
                f"$${self.credit_id}$$, "
                f"$${self.department}$$, "
                f"$${self.gender}$$, "
                f"$${self.job}$$, "
                f"$${self.name}$$, "
                f"$${self.profile_path}$$) ON CONFLICT (id) DO NOTHING")
