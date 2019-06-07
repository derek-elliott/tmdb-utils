#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import tmdb_utils.DataClasses as dc


def test_collection():
    collection = dc.Collection(1, 'Test Collection', '/my/poster/path', '/ma/backdrop/path')
    assert collection.get_insert_statement() == "INSERT INTO tmdb_collection VALUES(1, $$Test Collection$$, $$/my/poster/path$$, $$/ma/backdrop/path$$) ON CONFLICT (id) DO NOTHING"


def test_genre():
    genre = dc.Genre(1, 'Comedy')
    assert genre.get_insert_statement() == "INSERT INTO tmdb_genres VALUES(1, $$Comedy$$) ON CONFLICT (id) DO NOTHING"


def test_productioncompany():
    company = dc.ProductionCompany(1, 'ACME')
    assert company.get_insert_statement() == "INSERT INTO tmdb_production_companies VALUES(1, $$ACME$$) ON CONFLICT (id) DO NOTHING"


def test_country():
    country_with_id = dc.Country('US', 'USA', id=1)
    country_without_id = dc.Country('US', 'USA')
    assert country_with_id.get_insert_statement() == "INSERT INTO tmdb_countries VALUES(1, $$US$$, $$USA$$) ON CONFLICT (id) DO NOTHING"
    assert country_without_id.get_insert_statement() == "INSERT INTO tmdb_countries(iso_3166_1, name) VALUES($$US$$, $$USA$$) ON CONFLICT (id) DO NOTHING"
    assert country_with_id.get_id_query_statement() == "SELECT id FROM tmdb_countries WHERE iso_3166_1=US"


def test_language():
    language_with_id = dc.Language('EN', 'English', id =1)
    language_without_id = dc.Language('EN', 'English')
    assert language_with_id.get_insert_statement() == "INSERT INTO tmdb_languages VALUES(1, $$EN$$, $$English$$) ON CONFLICT (id) DO NOTHING"
    assert language_without_id.get_insert_statement() == "INSERT INTO tmdb_languages(iso_639_1, name) VALUES($$EN$$, $$English$$) ON CONFLICT (id) DO NOTHING"
    assert language_with_id.get_id_query_statement() == "SELECT id FROM tmdb_languages WHERE iso_639_1=EN"


def test_keyword():
    keyword = dc.Keyword(1, 'Time travel')
    assert keyword.get_insert_statement() == "INSERT INTO tmdb_keywords VALUES(1, $$Time travel$$) ON CONFLICT (id) DO NOTHING"


def test_cast():
    person = dc.Cast(1, 1, 1, 'abc123', 'John Doe/ Jane Doe/ Other', 1, 'John Doe', 1, '/path/to/profile')
    assert person.get_insert_statement() == "INSERT INTO tmdb_cast VALUES(1, 1, 1, $$abc123$$, ARRAY[$$John Doe$$, $$Jane Doe$$, $$Other$$], 1, $$John Doe$$, 1, $$/path/to/profile$$) ON CONFLICT (id) DO NOTHING"


def test_crew():
    person = dc.Crew(1, 1, 'abc123', 'Admin', 1, 'Director', 'John Doe', '/path/to/profile')
    assert person.get_insert_statement() == "INSERT INTO tmdb_crew VALUES(1, 1, $$abc123$$, $$Admin$$, 1, $$Director$$, $$John Doe$$, $$/path/to/profile$$) ON CONFLICT (id) DO NOTHING"
