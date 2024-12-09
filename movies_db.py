"""Modules to create DB"""
import random
import sys

# pylint: disable=import-error
import movies_csv_data  # type: ignore
from PySide2.QtSql import QSqlDatabase, QSqlQuery

# Create DB
db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("file/movies.db")

if not db.open():
    print("Unable to open data source file")
    sys.exit(1)

query = QSqlQuery()
# Delete Preexiting Tables
query.exec_("DROP TABLE movies")

query.exec_(
    """CREATE TABLE movies (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    film_id INTEGER NOT NULL,
    film_name VARCHAR(30) NOT NULL,
    genre VARCHAR(30) NOT NULL,
    lead_studio VARCHAR(40) NOT NULL,
    audience_score INTEGER NOT NULL,
    profitability REAL NOT NULL,
    rotten_tomatoes INTEGER NOT NULL,
    worldwide REAL NOT NULL,
    year INTEGER NOT NULL)"""
)

query.prepare(
    """INSERT INTO movies (film_id, film_name, genre, lead_studio, 
    audience_score, profitability, rotten_tomatoes, worldwide, year) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
)

film_ids = random.sample(range(1000, 2500), len(movies_csv_data.film_name))

query.exec_()

for idx, _ in enumerate(movies_csv_data.film_name):
    query.addBindValue(film_ids[idx])
    query.addBindValue(movies_csv_data.film_name[idx])
    query.addBindValue(movies_csv_data.genre[idx])
    query.addBindValue(movies_csv_data.lead_studio[idx])
    query.addBindValue(movies_csv_data.audience_score[idx])
    query.addBindValue(movies_csv_data.profitability[idx])
    query.addBindValue(movies_csv_data.rotten_tomatoes[idx])
    query.addBindValue(movies_csv_data.worldwide[idx])
    query.addBindValue(movies_csv_data.year[idx])
    query.exec_()

db.close()
