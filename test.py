import unittest
import app
import pdb
import random


class MyTestCase(unittest.TestCase):
    # def test_something(self):
    #     self.assertEqual(True, False)
    def setUp(self):
        self.app = app.app.test_client()

    def login(self):
        return self.app.post('/login', data=dict(
            email='aaa@ccc.com',
            password='123'
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login(self):
        rv = self.login()
        # pdb.set_trace()
        self.assertEqual(200, rv.status_code)

    def test_logout(self):
        rv = self.logout()
        self.assertEqual(200, rv.status_code)

    def test_regist(self):
        num = random.random()
        rv = self.app.post('/regist', data=dict(
            email="test{}@test.com".format(num),
            username="test",
            password1="123",
            password2="123"
        ), follow_redirects=True)
        self.assertEqual(200, rv.status_code)

    def test_question(self):
        self.login()
        rv = self.app.post('/question/', data=dict(
            title="TEST",
            content="This is a test for question"
        ), follow_redirects=True)
        self.assertEqual(200, rv.status_code)

    def test_answer(self):
        self.login()
        rv = self.app.post('/add_answer/', data=dict(
            question_id="103",
            answer_content="This is a test for answer"
        ), follow_redirects=True)
        self.assertEqual(200, rv.status_code)

    def test_detail(self):
        rv = self.app.get('/detail/103', follow_redirects=True)
        self.assertEqual(200, rv.status_code)

    def test_serach(self):
        rv = self.app.post('/search/', data=dict(
            search_key="一",
        ), follow_redirects=True)
        self.assertEqual(200, rv.status_code)

    def test_delete_question_user(self):
        self.login()
        rv = self.app.post('/delete_question_user/', data=dict(
            question_id_delete="100",
        ), follow_redirects=True)
        self.assertEqual(200, rv.status_code)

    def test_delete_question(self):
        self.login()
        rv = self.app.post('/delete_question/', data=dict(
            question_id_delete="100",
        ), follow_redirects=True)
        self.assertEqual(200, rv.status_code)

    def test_right(self):
        self.login()
        rv = self.app.post('/right/', data=dict(
            user_id="1",
            user_mute="1"
        ), follow_redirects=True)
        self.assertEqual(200, rv.status_code)

    def test_person_info(self):
        self.login()
        rv = self.app.get('/person_info/', follow_redirects=True)
        self.assertEqual(200, rv.status_code)

    def test_person_questions(self):
        self.login()
        rv = self.app.get('/person_questions/', follow_redirects=True)
        self.assertEqual(200, rv.status_code)

    def test_person_answers(self):
        self.login()
        rv = self.app.get('/person_answers/', follow_redirects=True)
        self.assertEqual(200, rv.status_code)

    def test_person_info_update(self):
        self.login()
        rv = self.app.post('/person_info_update/', data=dict(
            email="aaa@ccc.com",
            username="test",
            gender="男",
            school="cau",
        ), follow_redirects=True)
        self.assertEqual(200, rv.status_code)

    def test_person_info_update_test(self):
        self.login()
        rv = self.app.get('/person_info_update_test/', follow_redirects=True)
        self.assertEqual(200, rv.status_code)


if __name__ == '__main__':
    # suite = unittest.TestSuite()
    # suite.addTest(MyTestCase("test_regist"))
    # suite.addTest(MyTestCase("test_login"))
    # suite.addTest(MyTestCase("test_question"))
    # suite.addTest(MyTestCase("test_logout"))
    # unittest.TextTestRunner(verbosity=3).run(suite)
    unittest.main()
