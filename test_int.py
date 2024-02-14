import unittest
from app import app 

class TestArticleSearch(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_search_by_title(self):
        response = self.app.get("/prikaz_novosti?search_query=example_title")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"prikaz_novosti", response.data)

    def test_search_by_category(self):
        response = self.app.get("/prikaz_novosti?category=example_category")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"prikaz_novosti", response.data)

    def test_search_by_tag(self):
        response = self.app.get("/prikaz_novosti?search_query=example_tag")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"prikaz_novosti", response.data)

    def test_search_by_date(self):
        response = self.app.get("/prikaz_novosti?search_query=&category=&date=2022-01-01")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"prikaz_novosti", response.data)

if __name__ == "__main__":
    unittest.main()
