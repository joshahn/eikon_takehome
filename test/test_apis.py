#/usr/bin/env python

import requests
from parameterized import parameterized
from time import sleep
import unittest

class TestApi(unittest.TestCase):

    URL = "http://127.0.0.1:5500/api/v1/{method}{val}"
    GET_TOTAL_EXP = "get_total_experiments"
    GET_AVG_EXP_PER_USER = "get_average_experiment_per_user"
    GET_MOST_COMMON = "get_most_commonly_used_compound"
    ID = "id"
    EMAIL = "email"

    ASSERT_FAIL_MESSAGE_VALUE = "Expected {e}, but got {a}"
    ASSERT_FAIL_MESSAGE_LIST = "Expected {a} to be in {e}"

    # Convert Compound to compound_id
    COMPOUND_MAP = {
        "Compound A": 1,
        "Compound B": 2,
        "Compound C": 3
    }

    @classmethod
    def setUpClass(cls):
       resp = requests.post("http://127.0.0.1:5500/api/v1/load")
       sleep(2)


    # HELPER FUNCTIONS
    def get_request(self, method, how, val):
        if how == self.EMAIL:
            value = "?email={e}".format(e=val)
        elif how == self.ID:
            value = "?user_id={i}".format(i=val)
        if value:
            return requests.get(self.URL.format(method=method, val=value))
        else:
            return None


    # TEST GET TOTAL EXPERIMENT FOR USER
    @parameterized.expand([
        (1, 2),
        (2, 1),
        (3, 1),
        (10, 1)
    ])
    def test_get_total_experiments_valid_user_id(self, user_id, expected):
        resp = self.get_request(self.GET_TOTAL_EXP, self.ID, user_id)
        assert resp.status_code == 200
        resp_json = resp.json()
        try:
            exp_num = int(resp_json["value"])
        except:
            assert False, "Couldn't convert to int"
        assert exp_num == expected, self.ASSERT_FAIL_MESSAGE_VALUE.format(e=expected, a=exp_num)

    @parameterized.expand([
        (0, 400),
        (99, 404),
        (-1, 400),
        ("a", 400),
        (None, 400)
    ])
    def test_get_total_experiments_invalid_user_id(self, user_id, error_code):
        resp = self.get_request(self.GET_TOTAL_EXP, self.ID, user_id)
        resp_json = resp.json()
        assert resp.status_code == error_code

    @parameterized.expand([
        ("alice@example.com", 2),
        ("dave@example.com", 1),
        ("grace@example.com", 1)
    ])
    def test_get_total_experiments_valid_email(self, email, expected):
        resp = self.get_request(self.GET_TOTAL_EXP, self.EMAIL, email)
        assert resp.status_code == 200
        resp_json = resp.json()
        try:
            exp_num = int(resp_json["value"])
        except:
            assert False, "Couldn't convert to int"
        assert exp_num == expected, self.ASSERT_FAIL_MESSAGE_VALUE.format(e=expected, a=exp_num)

    @parameterized.expand([
        ("wrong@example.com", 404),
        (100, 404),
        (0, 404),
        ("@.com", 404),
        (None, 404)
    ])
    def test_get_total_experiments_invalid_email(self, email, error_code):
        resp = self.get_request(self.GET_TOTAL_EXP, self.EMAIL, email)
        resp_json = resp.json()
        assert resp.status_code == error_code


    # TEST GET AVERAGE EXPERIEMENT PER USER
    def test_handle_get_average_experiment_per_user(self):
        expected_avg = 1.1
        resp = requests.get(self.URL.format(method=self.GET_AVG_EXP_PER_USER,
                                            val=""))
        assert resp.status_code == 200
        resp_json = resp.json()
        assert resp_json["value"] == expected_avg, \
            self.ASSERT_FAIL_MESSAGE_VALUE.format(e=expected_avg, a=resp_json["value"])


    # TEST GET MOST COMMON COMPOUND FOR USER
    @parameterized.expand([
        (1, [2]),
        (2, [1,3]),
        (3, [2,3]),
        (10, [1,3])
        
    ])
    def test_get_most_common_valid_user_id(self, user_id, expected):
        resp = self.get_request(self.GET_MOST_COMMON, self.ID, user_id)
        assert resp.status_code == 200
        resp_json = resp.json()
        most_common_compound = resp_json["value"]
        assert most_common_compound in self.COMPOUND_MAP.keys(), "Invalid Compound: {}".format(most_common_compound)
        c_id = self.COMPOUND_MAP[most_common_compound]
        assert c_id in expected, self.ASSERT_FAIL_MESSAGE_LIST.format(e=expected, a=c_id)

    @parameterized.expand([
        (0, 400),
        (99, 404),
        (-1, 400),
        ("a", 400),
        (None, 400)
    ])
    def test_get_most_common_invalid_user_id(self, user_id, error_code):
        resp = self.get_request(self.GET_MOST_COMMON, self.ID, user_id)
        resp_json = resp.json()
        assert resp.status_code == error_code


    @parameterized.expand([
        ("alice@example.com", [2]),
        ("dave@example.com", [1, 2, 3]),
        ("grace@example.com", [2, 3])
    ])
    def test_get_most_common_valid_email(self, email, expected):
        resp = self.get_request(self.GET_MOST_COMMON, self.EMAIL, email)
        assert resp.status_code == 200
        resp_json = resp.json()
        most_common_compound = resp_json["value"]
        assert most_common_compound in self.COMPOUND_MAP.keys(), "Invalid Compound: {}".format(most_common_compound)
        c_id = self.COMPOUND_MAP[most_common_compound]
        assert c_id in expected, self.ASSERT_FAIL_MESSAGE_LIST.format(e=expected, a=c_id)

    @parameterized.expand([
        ("wrong@example.com", 404),
        (100, 404),
        (0, 404),
        ("@.com", 404),
        (None, 404)
    ])
    def test_get_most_common_invalid_email(self, email, error_code):
        resp = self.get_request(self.GET_MOST_COMMON, self.EMAIL, email)
        resp_json = resp.json()
        assert resp.status_code == error_code

    