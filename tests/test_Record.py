from tmdb_utils.Record import Record
from typing import Any, List
import json


class MockDB:
    def __init__(self, query_result: Any, query_result_list: List[Any], return_error: str = False):
        self.query_result = query_result
        self.query_result_list = query_result_list
        self.return_error = return_error

    def execute_insert(self, statement: str) -> bool:
        if self.return_error:
            return False
        else:
            return True

    def execute_query(self, statement: str) -> List[Any]:
        if self.return_error:
            return None
        else:
            return self.query_result_list

    def execute_query_for_one(self, statement: str) -> Any:
        if self.return_error:
            return None
        else:
            return self.query_result


def test_from_dict():
    with open('test_data/test_record.json', 'r') as f:
        raw_dict = json.load(f)
    record = Record.from_dict(raw_dict)
    assert record is not None


def test_get_movie_insert_statement():
    with open('test_data/test_record.json', 'r') as f:
        raw_dict = json.load(f)
    record = Record.from_dict(raw_dict)
    assert record.get_movie_insert_statement() == ("INSERT INTO tmdb_movies VALUES(1, "
                                                   "313576, "
                                                   "14000000, "
                                                   "ARRAY [35], "
                                                   "$$$$, "
                                                   "tt2637294, "
                                                   "en, "
                                                   "$$Hot Tub Time Machine 2$$, "
                                                   "$$When Lou, who has become the \"father of the Internet,\" is shot by an unknown assailant, Jacob and Nick fire up the time machine again to save their friend.$$, "
                                                   "6.575393, "
                                                   "$$/tQtWuwvMf0hCc2QR2tkolwl7c3c.jpg$$, "
                                                   "ARRAY [4, 60, 8411], "
                                                   "ARRAY [], "
                                                   "2015-02-20, "
                                                   "93, "
                                                   "ARRAY [], "
                                                   "$$Released$$, "
                                                   "$$The Laws of Space and Time are About to be Violated.$$, "
                                                   "$$Hot Tub Time Machine 2$$, "
                                                   "ARRAY [4379, 9663, 11830, 179431], "
                                                   "12314651) ON CONFLICT (id) DO NOTHING")

