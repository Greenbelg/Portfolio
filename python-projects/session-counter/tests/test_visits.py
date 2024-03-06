import unittest
from datetime import date
import sys
import os
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from src.database import Database
from src.visits import Visits


class TestVisits(unittest.TestCase):
    def prepare_db(test_func):
        def wrapper(*args, **kwrags):
            real_db = Visits._db_visits
            Visits._db_visits = Database(
                Path(__file__).parent.parent.joinpath("visits"),
                "test_visits")
            test_func(*args, **kwrags)
            Visits._db_visits.clear()
            Visits._db_visits = real_db

        return wrapper

    def test_jsonize_data(self):
        result = Visits.jsonize_data(
            {'1': 2, '2': 3},
            {'1': 1, '2': 2},
            "day")

        expected_result = {
            "All visits for day": {'1': 2, '2': 3},
            "Unique visits for day": {'1': 1, '2': 2}
        }
        self.assertEqual(result, expected_result)

    @prepare_db
    def test_get_records(self):
        ip = "127.0.0.1"
        Visits.add_new_visit(ip)
        Visits.add_new_visit(ip)
        total_records, unique_records = Visits._get_records("visitor_ip")

        for i in range(2):
            self.assertEqual(total_records[i][0], ip)
        for i in range(1):
            self.assertEqual(unique_records[i][0], ip)

        self.assertEqual(len(unique_records), 1)

    @prepare_db
    def test_add_new_visit(self):
        ip = "127.0.0.1"
        Visits.add_new_visit(ip)

        self.assertEqual(Visits._db_visits.select(
            '''SELECT * FROM visits ORDER BY ID DESC LIMIT 1''')[0],
            (1, str(date.today().year),
             str(date.today().month), str(date.today().day),
             Database.WEEK_DAYS[date.today().weekday()], ip))


if __name__ == '__main__':
    unittest.main()
