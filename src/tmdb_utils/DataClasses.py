"""Dataclasses for elements of a TMDB record

Defines objects for parts of a TMDB record and provides insert statements for Postgres

"""
from dataclasses import dataclass
from typing import List

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

    def get_id_query_statement(self) -> str:
        """Generates a query statement for the Country object

        Returns:
            Country query string
        """
        return f"SELECT id FROM {self.table_name} WHERE iso_3166_1={self.iso_3166_1}"


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

    def get_id_query_statement(self) -> str:
        """Generates a query statement for the Language object

        Returns:
            Language query string
        """
        return f"SELECT id FROM {self.table_name} WHERE iso_639_1={self.iso_639_1}"


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
                f"{self.gender}, "
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
                f"{self.gender}, "
                f"$${self.job}$$, "
                f"$${self.name}$$, "
                f"$${self.profile_path}$$) ON CONFLICT (id) DO NOTHING")
