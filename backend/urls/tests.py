import unittest
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
import utils

class TestSEOAnalyzer(unittest.TestCase):

    def setUp(self):
        self.sample_html = """
        <html>
            <head>
                <title>Test Page</title>
                <meta name="description" content="Test description"/>
            </head>
            <body>
                <h1>Main Title</h1>
                <h2>Subheading</h2>
                <p>This is a test page.</p>
                <img src="test.jpg" alt=""/>
            </body>
        </html>
        """
        self.soup = BeautifulSoup(self.sample_html, "html.parser")

    @patch('utils.requests.get')
    def test_get_soup(self, mock_get):
        mock_get.return_value = Mock(content=self.sample_html)
        url = "http://example.com"
        soup = utils.get_soup(url)
        self.assertIsInstance(soup, BeautifulSoup)
        self.assertEqual(soup.title.string, "Test Page")

    def test_analyze_head(self):
        results = utils.analyze_head(self.soup)
        expected_results = {
            "title_exist": 1,
            "title_length": 9,
            "description_exist": 1
        }
        self.assertEqual(results, expected_results)

    def test_analyze_h_tags_order(self):
        result = utils.analyze_h_tags_order(self.soup)
        self.assertEqual(result, 1)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="the\nis\nand")
    def test_get_keywords(self, mock_open):
        keywords = utils.get_keywords(self.soup)
        self.assertIsInstance(keywords, dict)
        self.assertGreater(len(keywords), 0)

    def test_analyze_body(self):
        results = utils.analyze_body(self.soup)
        self.assertEqual(results["h1_exist"], 1)
        self.assertEqual(results["h_tags_order"], 1)
        self.assertEqual(results["h1_count"], 1)
        self.assertEqual(results["img_alt"], 1)

    @patch('utils.get_soup')
    def test_analyze_url(self, mock_get_soup):
        mock_get_soup.return_value = self.soup
        url = "http://example.com"
        results = utils.analyze_url(url)
        expected_results = {
            "title_exist": 1,
            "title_length": 9,
            "description_exist": 1,
            "h1_exist": 1,
            "h_tags_order": 1,
            "h1_count": 1,
            "img_alt": 1,
            "key_words": utils.get_keywords(self.soup),
            "url": url
        }
        self.assertEqual(results, expected_results)

if __name__ == '__main__':
    unittest.main()
