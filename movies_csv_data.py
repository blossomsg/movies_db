"""Modules to open CSV"""
import csv

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
