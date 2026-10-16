import sqlite3
import time


class ObservationDatabase:
    def __init__(self, db_name="observations.db"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        connection = sqlite3.connect(self.db_name)

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT NOT NULL,
                observer TEXT NOT NULL,
                filter_name TEXT,
                exposure REAL NOT NULL,
                observation_type TEXT,
                wavelength REAL,
                date TEXT
            )
        """)

        connection.commit()
        connection.close()

    def add_observation(self, observation):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        wavelength = getattr(observation, "wavelength", None)
        observation_type = type(observation).__name__

        cursor.execute("""
            INSERT INTO observations
            (target, observer, filter_name, exposure,
             observation_type, wavelength, date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            observation.target,
            observation.observer,
            observation.filter,
            observation.exposure,
            observation_type,
            wavelength,
            time.strftime("%Y-%m-%d")
        ))

        connection.commit()
        connection.close()

    def show_observations(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM observations")
        rows = cursor.fetchall()

        connection.close()

        return rows

    def search_observation(self, target):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM observations WHERE target = ?",
            (target,)
        )

        rows = cursor.fetchall()
        connection.close()

        return rows

    def export_to_csv(self, filename="observations.csv"):
        import csv

        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM observations")
        rows = cursor.fetchall()

        columns = [
            "id",
            "target",
            "observer",
            "filter_name",
            "exposure",
            "observation_type",
            "wavelength",
            "date"
        ]

        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(columns)
            writer.writerows(rows)

        connection.close()

    def import_from_csv(self, filename="observations.csv"):
        import csv

        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        imported_count = 0

        with open(filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM observations
                    WHERE target = ?
                    AND observer = ?
                    AND filter_name = ?
                    AND exposure = ?
                    AND observation_type = ?
                    AND wavelength = ?
                    AND date = ?
                    """,
                    (
                        row["target"],
                        row["observer"],
                        row["filter_name"],
                        row["exposure"],
                        row["observation_type"],
                        row["wavelength"] or None,
                        row["date"],
                    ),
                )

                if cursor.fetchone()[0] == 0:
                    cursor.execute(
                        """
                        INSERT INTO observations
                        (target, observer, filter_name, exposure,
                         observation_type, wavelength, date)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            row["target"],
                            row["observer"],
                            row["filter_name"],
                            float(row["exposure"]),
                            row["observation_type"],
                            row["wavelength"] or None,
                            row["date"],
                        ),
                    )
                    imported_count += 1

        connection.commit()
        connection.close()

        return imported_count



