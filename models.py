from playhouse.postgres_ext import *
import datetime


psql_db = PostgresqlExtDatabase(
    'songkick', # required by peewee
    user = 'mark', # will be passed to psycopg2
    #password = 'secret', # ditto
    #host = 'localhost', # ditto
)

class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = psql_db

class Venue(BaseModel):
    venue_id = IntegerField(primary_key=True)
    google_id = CharField(null=True)
    name = CharField(unique=True)
    city = CharField(null=True)
    state = CharField(null=True)
    country = CharField(null=True)
    lat = FloatField(null=True)
    lng = FloatField(null=True)
    street = CharField(null=True)
    zip_code = CharField(null=True)
    phone = CharField(null=True)
    url = CharField(null=True)
    description = TextField(null=True)
    capacity = IntegerField(null=True)
    created = DateTimeField(null=True)
    modified = DateTimeField(null=True)

    class Meta:
        table_alias = 'venues'

class Event(BaseModel):
    venue = ForeignKeyField(Venue, related_name='events')
    #artists = ManyToManyField(Artist, related_name='events')
    event_id = IntegerField(primary_key=True)
    name = CharField(null=True)
    type = CharField(null=True)
    status = CharField(null=True)
    datetime = DateTimeField(null=True)
    url = CharField(null=True)
    popularity = FloatField(null=True)
    created = DateTimeField(null=True)
    modified = DateTimeField(null=True)

    class Meta:
        table_alias = 'events'
        indexes = (
            # create a unique on name and datetime
            (('event_id', 'name', 'datetime'), True),
        )

class Artist(BaseModel):
    artist_id = IntegerField(primary_key=True)
    name = CharField(unique=True)
    echonest_response = JSONField(null=True)
    spotify_response = JSONField(null=True)
    genres = JSONField(null=True)
    location = HStoreField(null=True)
    spotify_id = CharField(null=True)
    familiarity = CharField(null=True)
    hotttnesss = CharField(null=True)
    discovery = CharField(null=True)
    years_active = JSONField(null=True)
    term1 = CharField(null=True)
    term2 = CharField(null=True)
    genre1 = CharField(null=True)
    genre2 = CharField(null=True)
    created = DateTimeField(null=True)
    modified = DateTimeField(null=True)

    class Meta:
        table_alias = 'artists'

class Performance(BaseModel):
    artist = ForeignKeyField(Artist)
    event = ForeignKeyField(Event)
    billing = CharField(null=True)
    billing_index = IntegerField(null=True)
