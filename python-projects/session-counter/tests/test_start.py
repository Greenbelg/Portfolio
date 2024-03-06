import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from start import app, initialize_dash


class TestStart(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        initialize_dash()

    def test_start_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_stats_page_with_valid_period(self):
        response = self.app.get('/stats/day')
        self.assertEqual(response.status_code, 200)

    def test_stats_page_with_invalid_period(self):
        response = self.app.get('/stats/some_strange_period')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
