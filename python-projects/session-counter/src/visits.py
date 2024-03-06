from datetime import date
from pathlib import Path

from src.database import Database


class Visits:
    _db_visits = Database(Path(__file__).parent.parent.joinpath("visits"),
                          "visits")

    def get_stats_for(period):
        db_column = Database.TABLE_NAMES[period]
        all_records, unique_records = Visits._get_records(db_column)
        all_count = Visits._handle_data_from_table(all_records)
        unique_count = Visits._handle_data_from_table(unique_records)
        return all_count, unique_count

    def jsonize_data(all_data, unique_data, period):
        return {
            f"All visits for {period}": all_data,
            f"Unique visits for {period}": unique_data
        }

    def _handle_data_from_table(data):
        return {str(key[0]): data.count(key) for key in set(data)}

    def _get_records(column):
        total_records = Visits._db_visits.select(
            f'SELECT {column} FROM visits')
        unique_records = Visits._db_visits.select(
            f'SELECT {column} FROM visits GROUP BY {column}, visitor_ip')
        return total_records, unique_records

    def add_new_visit(ip):
        Visits._db_visits.insert(
            date.today().year,
            date.today().month,
            date.today().day,
            date.today().weekday(),
            ip)
