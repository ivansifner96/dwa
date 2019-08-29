from pony import orm
from pony.orm import Database, PrimaryKey, Required, Set, db_session, Optional
from uuid import uuid4
import datetime as dt
from decimal import Decimal
import os

db =orm.Database()
db.bind(provider='sqlite',filename='baza.sqlite',create_db=True)


class Korisnik(db.Entity):
	email = orm.Required(str)
	username = orm.Required(str)
	password = orm.Required(str)

class Zapisnik(db.Entity):
	naziv_filma = orm.Required(str)
	godina = orm.Required(int)
	datum_pregleda = Required(dt.datetime)
	korisnik_mail = orm.Required(str)

db.generate_mapping(create_tables=True, check_tables=True)


