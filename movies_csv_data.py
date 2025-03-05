"""Modules to open CSV"""

import csv

# pylint: disable=import-error
from utils import fix_wrong_spellings

# Storing all the CSV columns data in the lists.
film_name = []
genre = []
lead_studio = []
audience_score = []
profitability = []
rotten_tomatoes = []
worldwide = []
year = []

with open("movies.csv", "r", encoding="UTF-8") as m:
    file = csv.DictReader(m)
    for data in file:
        film_name.append(data["Film"])
        genre.append(data["Genre"])
        lead_studio.append(data["Lead Studio"])
        audience_score.append(data["Audience score %"])
        profitability.append(data["Profitability"])
        rotten_tomatoes.append(data["Rotten Tomatoes %"])
        worldwide.append(data["Worldwide Gross"][1:])
        year.append(data["Year"])

# Fix spelling mistakes
# print(Counter(genre))
# Counter({'Comedy': 41, 'Romance': 13, 'Drama': 13, 'Animation': 4,
# 'Fantasy': 1, 'Romence': 1, 'Comdy': 1,
# 'Action': 1, 'romance': 1, 'comedy': 1})

# pylint: disable=invalid-name
comedy_pattern = "comedy|Comdy"
fix_wrong_spellings.fix_spellings(
    pattern=comedy_pattern, column_category=genre, new_name="Comedy"
)
# pylint: disable=invalid-name
romance_pattern = "romance|Romence"
fix_wrong_spellings.fix_spellings(
    pattern=romance_pattern, column_category=genre, new_name="Romance"
)
