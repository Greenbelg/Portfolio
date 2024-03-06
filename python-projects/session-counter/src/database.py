import sqlite3


class Database:
    TABLE_NAMES = {
        "all": "visitor_ip",
        "year": "year",
        "month": "month",
        "week": "days_in_week",
        "day": "day"
    }

    WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday",
                 "Friday", "Saturday", "Sunday"]

    def __init__(self, path_to_db, name_db):
        self.conn = sqlite3.connect(path_to_db.joinpath(name_db + ".db"),
                                    check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS visits (
                id INTEGER PRIMARY KEY,
                year TEXT,
                month TEXT,
                day TEXT,
                visitor_ip TEXT
            )''')
        self.conn.commit()

    def close(self):
        self.conn.close()

    def insert(self, year, month, day, day_in_week, ip):
        self.cursor.execute('''
                INSERT INTO visits
                (year, month, day, visitor_ip, days_in_week)
                VALUES (?, ?, ?, ?, ?)
            ''', (str(year), str(month), str(day), ip,
                  Database.WEEK_DAYS[day_in_week]))
        self.conn.commit()

    def select(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def clear(self):
        self.cursor.execute("DELETE FROM visits")
        self.conn.commit()
