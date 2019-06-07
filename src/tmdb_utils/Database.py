import psycopg2
from typing import List, Any


class Database:
    """Utility functions for Postgres, wraps psycopg2 functionality"""

    def __init__(self, user: str, password: str, db_name: str, host: str, port: int):
        self.user = user  #: Username for database
        self.password = password  #: Password for database
        self.db_name = db_name  #: Name of the database
        self.host = host  #: Database hostname
        self.port = port  #: Database port
        self.connection = psycopg2.connect(f'host={self.host} dbname={self.db_name} user={self.user} '
                                           f'password={self.password}')  #: Database connection

    def execute_insert(self, statement: str) -> bool:
        """Executes an insert command

        Args:
            statement: The insert statement to execute

        Returns:
            True if there was no error, False otherwise
        """
        cur = self.connection.cursor()
        try:
            cur.execute(statement)
        except Exception as e:
            print(f'Error executing insert statement: {statement} with error: {e}')
            self.connection.rollback()
            return False
        self.connection.commit()
        return True

    def execute_query(self, statement: str) -> List[Any]:
        """Executes a query statement

        Args:
            statement:  The query statement to execute

        Returns:
            A list of tuples with the result of the query, or None if an error occurred.
        """
        cur = self.connection.cursor()
        try:
            cur.execute(statement)
        except Exception as e:
            print(f'Error executing insert statement: {statement} with error: {e}')
            self.connection.rollback()
            return None
        self.connection.commit()
        return [item for item in cur]

    def execute_query_for_one(self, statement: str) -> Any:
        """Executes a query statement that returns a single item

                Args:
                    statement:  The query statement to execute

                Returns:
                    A tuple with the result of the query, or None if an error occurred.
                """
        cur = self.connection.cursor()
        try:
            cur.execute(statement)
        except Exception as e:
            print(f'Error executing insert statement: {statement} with error: {e}')
            self.connection.rollback()
            return None
        self.connection.commit()
        data = list(cur)
        if len(data) == 0:
            return None
        else:
            return data[0][0]

    def set_up_tables(self):
        """Creates the tables needed for the TMDB database"""
        commands = ['DROP TABLE tmdb_movies, tmdb_collection, tmdb_genres, tmdb_production_companies, tmdb_countries, tmdb_languages, tmdb_keywords, tmdb_cast, tmdb_crew;',
                    """CREATE TABLE IF NOT EXISTS tmdb_movies (
    id integer PRIMARY KEY,
    collection_id integer,
    budget integer,
    genre_ids integer ARRAY,
    homepage varchar(255),
    imdb_id varchar(20),
    original_language_id integer ARRAY,
    original_title varchar(255),
    overview varchar(255),
    popularity numeric,
    poster_path varchar(255),
    production_company_ids integer ARRAY,
    production_country_ids integer ARRAY,
    release_date date,
    runtime numeric,
    spoken_language_ids integer ARRAY,
    status varchar(10),
    tagline varchar(255),
    title varchar(255),
    keyword_ids integer ARRAY,
    revenue integer
);
                    """,
                    """CREATE TABLE IF NOT EXISTS tmdb_collection (
    id integer PRIMARY KEY,
    name varchar(255),
    poster_path varchar(255),
    backdrop_path varchar(255)
);
                    """,
                    """CREATE TABLE IF NOT EXISTS tmdb_genres (
    id integer PRIMARY KEY,
    name varchar(50)
);
                    """,
                    """CREATE TABLE IF NOT EXISTS tmdb_production_companies (
    id integer PRIMARY KEY,
    name varchar(255)
);
                    """,
                    """CREATE TABLE IF NOT EXISTS tmdb_countries (
    id serial PRIMARY KEY,
    iso_3166_1 varchar(2) UNIQUE,
    name varchar(255)
);
                    """,
                    """CREATE TABLE IF NOT EXISTS tmdb_languages (
    id serial PRIMARY KEY,
    iso_639_1 varchar(2) UNIQUE,
    name varchar(255)
);
                    """,
                    """CREATE TABLE IF NOT EXISTS tmdb_keywords (
    id integer PRIMARY KEY,
    name varchar(255)
);
                    """,
                    """CREATE TABLE IF NOT EXISTS tmdb_cast (
    id integer,
    movie_id integer REFERENCES tmdb_movies(id),
    cast_id integer,
    credit_id varchar(255),
    character varchar(255) ARRAY,
    gender int,
    name varchar(255),
    "order" integer,
    profile_path varchar(255),
    PRIMARY KEY (id)
);
                    """,
                    """CREATE TABLE IF NOT EXISTS tmdb_crew (
    id integer,
    movie_id integer REFERENCES tmdb_movies(id),
    credit_id varchar(255),
    department varchar(255),
    gender int,
    job varchar(255),
    name varchar(255),
    profile_path varchar(255),
    PRIMARY KEY (id)
);
                    """
                    ]
        for command in commands:
            self.execute_insert(command)

    def drop_all_tables(self):
        """Drops all TMDB tables from Postgres"""
        self.execute_insert("""DROP TABLE tmdb_movies, tmdb_collection, tmdb_genres, tmdb_production_companies, tmdb_countries, tmdb_languages, tmdb_keywords, tmdb_cast, tmdb_crew;""")

    def __del__(self):
        self.connection.close()
