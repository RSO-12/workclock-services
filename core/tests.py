import unittest
from core.token import *
from core.util import generate_random_pass
from app import app


class TestTokenFunctions(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

        token = generate_token(user_id=123, is_admin=True)
        headers = {'Authorization': f'Bearer {token}'}
        self.admin_header = headers

        token = generate_token(user_id=234, is_admin=False)
        headers = {'Authorization': f'Bearer {token}'}
        self.user_header = headers

    def test_generate_token(self):
        token = generate_token(user_id=123, is_admin=False)
        self.assertIsNotNone(token)

        token = generate_token(user_id=500, is_admin=True)
        self.assertIsNotNone(token)

    def test_request_no_token_req(self):
        response = self.app.get('/v1/mock/test', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/v1/mock/test', headers=self.user_header)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/v1/mock/test')
        self.assertEqual(response.status_code, 200)

    def test_request_token(self):
        response = self.app.get('/v1/mock/token-test', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/v1/mock/token-test', headers=self.user_header)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/v1/mock/token-test')
        self.assertEqual(response.status_code, 401)

    def test_request_token_admin(self):
        response = self.app.get('/v1/mock/token-admin-test', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/v1/mock/token-admin-test', headers=self.user_header)
        self.assertEqual(response.status_code, 403)

        response = self.app.get('/v1/mock/token-admin-test')
        self.assertEqual(response.status_code, 401)

    def test_get_random_pass(self):
        for i in range(10):
            passwd = generate_random_pass()
            self.assertTrue(isinstance(passwd, str))
            self.assertTrue(len(passwd) > 10)
            self.assertTrue(' ' not in passwd)


if __name__ == '__main__':
    unittest.main()
