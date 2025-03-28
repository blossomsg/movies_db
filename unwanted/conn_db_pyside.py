from encodings.quopri_codec import quopri_encode

from PySide2.QtSql import QSqlDatabase, QSqlQuery


# Create DB
db = QSqlDatabase.addDatabase("QPSQL")
db.setDatabaseName("movies")
db.setHostName("localhost")
db.setUserName("postgres")
db.setPassword("123456789")
db.setPort(5432)
db.open()
query = QSqlQuery("SELECT * FROM movies")
# rec = query.result()
# # namecol = rec.indexOf("genre")
# if query.next():
#     print(query.record().keyValues())
rec = query.record()
if query.next():
    print(query.record().keyValues(rec))

# print(namecol)
# # while query.next():
#     print(query.value(namecol).toString())

db.close()


