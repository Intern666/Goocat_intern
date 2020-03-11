import unittest
import app
import pdb


class MyTestCase(unittest.TestCase):
    # def test_something(self):
    #     self.assertEqual(True, False)
    def setUp(self):
        self.app = app.app.test_client()

    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('aaa@bbb.com', '123')
        # pdb.set_trace()
        self.assertEqual(200, rv.status_code)


if __name__ == '__main__':
    unittest.main()
