import os
from datetime import datetime
from peewee import *

database = SqliteDatabase('database.db')

class BaseModel(Model):

	class Meta:
		database = database

class Entry(BaseModel):
	wallet = CharField(unique=True, max_length=34)
	private_key = CharField(max_length=64)
	balance = FloatField(null=True)
	timestamp = DateTimeField(default=datetime.now(), null=True)