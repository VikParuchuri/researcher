from datetime import datetime

from peewee import Model, SqliteDatabase, TextField, IntegerField, ForeignKeyField, DateTimeField

db = SqliteDatabase('links.db')


class Query(Model):
    query = TextField()
    created = DateTimeField(default=datetime.now)

    class Meta:
        database = db


class Link(Model):
    link = TextField()
    rank = IntegerField()
    html = TextField()
    created = DateTimeField(default=datetime.now)
    query = ForeignKeyField(Query, backref="links")

    class Meta:
        database = db


db.create_tables([Query, Link])
