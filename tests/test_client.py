# coding=utf-8
from unittest import TestCase
from datetime import datetime
import httpretty
from urbanpyctionary.client import Client
from urbanpyctionary.errors import *
from tests.mocks import *

CORRECT_APIKEY = "mdBwYTF7RMKVQK2YtZKFPRsmW2gdBX59GBMDbz5MSFeABGeW3f"
INCORRECT_APIKEY = "mdBwYTF7RMKVQK2YtZKFPRsmW2gdBX59GBMDbz5MSFeABGeW4f"
MALFORMED_APIKEY_SH = "mdBwYTF7RMKVQK2YtZKFPRsmW2gdBX59GBMDbz5MSFeABGeW3"
MALFORMED_APIKEY_LO = "mdBwYTF7RMKVQK2YtZKFPRsmW2gdBX59GBMDbz5MSFeABGeW3fff"

class APIKeyErrorsTestCase(TestCase):

    @httpretty.activate
    def test_returning_invalid_auth(self):
        httpretty.register_uri(httpretty.GET,
                               "https://mashape-community-urban-dictionary.p.mashape.com/define?term=python",
                               body='',
                               status=403)

        c = Client(API_key=INCORRECT_APIKEY)

        with self.assertRaises(APIError):
            c.get("python")

    def test_malformed_apikeys_too_short(self):

        with self.assertRaises(MalformedAPIKey):
            c = Client(API_key=MALFORMED_APIKEY_SH)

    def test_malformed_apikeys_too_long(self):

        with self.assertRaises(MalformedAPIKey):
            c = Client(API_key=MALFORMED_APIKEY_LO)

    def test_no_api_key(self):

        with self.assertRaises(MalformedAPIKey):
            c = Client()

    def test_correct_client_generation(self):

        c = Client(CORRECT_APIKEY)

        self.assertIsInstance(c, Client)


class RequestsTestCase(TestCase):

    @httpretty.activate
    def test_request_body(self):
        httpretty.register_uri(httpretty.GET,
                               "https://mashape-community-urban-dictionary.p.mashape.com/define?term=python",
                               body=python_rbody,
                               type='application/json',
                               status=200)

        c = Client(CORRECT_APIKEY)
        resp = c.get("python")

        assert(len(resp) == 2)
        assert(len(resp.tags) == 4)
        assert(resp.word == "python")

        def1 = resp.definitions[0]
        assert(def1.author == "steak")
        assert(def1.defid == 192074)
        assert isinstance(def1.definition, str)
        assert isinstance(def1.example, str)
        assert def1.permalink.endswith(str(def1.defid))
        assert isinstance(def1.time_acquired, datetime)
