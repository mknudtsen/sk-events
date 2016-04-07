from models import Venue, Event, Artist, Performance, psql_db
from utils import get_venues, get_artists, SONGKICK, ECHONEST, get_terms


import requests
import random
import time
import os


def create_tables():
    psql_db.connect()
    psql_db.create_tables([Venue, Event, Artist, Performance], safe=True)

def update_venues(venue_ids):

    for identifier in venue_ids:
        payload = {'apikey': SONGKICK}
        url = 'http://api.songkick.com/api/3.0/venues/'+str(identifier)+'.json?'

        r = requests.get(url, params=payload)
        data = r.json()
        results = data['resultsPage']['results']['venue']

        try:
        	venue_id = results['id']
        	name = results['displayName']
        	city = results['city']['displayName']
        	state = results['city']['state']['displayName']
        	country = results['city']['country']['displayName']
        	lat = results['lat']
        	lng = results['lng']
        	street = results['street']
        	zip_code = results['zip']
        	phone = results['phone']
        	url = results['website']
        	capacity = results['capacity']
        except IntegrityError, error:
        	print 'An error occured: %s' % error
        	pass
        except KeyError, error:
        	print 'An error occured: %s' % error
        	pass

        venue, _created = Venue.get_or_create(venue_id=venue_id, name=name)
        venue.city = city
        venue.state = state
        venue.country = country
        venue.lat = lat
        venue.lng = lng
        venue.street = street
        venue.zip_code = zip_code
        venue.phone = phone
        venue.url = url
        venue.capacity = capacity
        print venue.name
        venue.save()

        time.sleep(1)


def update_events(venue_ids):

    for identifier in venue_ids:
    	payload = {'apikey': SONGKICK, 'per_page': 50, 'page': 1}
    	url = 'http://api.songkick.com/api/3.0/venues/'+str(identifier)+'/calendar.json?'

    	r = requests.get(url, params=payload)
    	r.raise_for_status()
    	data = r.json()

    	venue = Venue.get(venue_id=identifier)
    	#venue.save()

    	try:
    		results = data['resultsPage']['results']['event']
    	except KeyError, error:
    		print 'An error occured: %s: There are no upcoming events for this venue: %s' % (error, venue.name)
    		continue

    	for item in results:
            try:
                event_id = item['id']
                name = item['displayName']
                type = item['type']
                status = item['status']
                datetime = item['start']['datetime']
                url = item['uri']
                popularity = item['popularity']
            except KeyError, error:
                print 'An error occured: %s: There is limited data for event: %s' % (error, event_id)
                pass

            event, _created = Event.get_or_create(event_id=event_id, venue=venue)
            event.name = name
            event.type = type
            event.status = status
            event.datetime = datetime
            event.url = url
            event.popularity = popularity
            print event.name
            event.save()

            for artist in item['performance']:
                try:
                    artist_id = artist['artist']['id']
                    name = artist['artist']['displayName']
                    performer, _created = Artist.get_or_create(artist_id=artist_id, name=name)
                    billing = artist['billing']
                    billing_index = artist['billingIndex']
                    p, _created = Performance.get_or_create(artist=performer, event=event)
                    p.billing = billing
                    p.billing_index = billing_index
                    p.save()

                except KeyError, error:
                    print 'An error occured %s' % error
                    pass

        time.sleep(1)


def update_artists(artist_ids):

    for artist in artist_ids:
    	payload = {'api_key': ECHONEST, 'id': 'songkick:artist:'+str(artist)+'',
        'format': 'json', 'bucket': ['genre', 'id:spotify-WW', 'familiarity',
        'discovery', 'hotttnesss', 'artist_location', 'years_active']}
    	url = 'http://developer.echonest.com/api/v4/artist/profile?'

    	r = requests.get(url, params=payload)
    	data = r.json()
        # retrieve the artist record from the db
        artist = Artist.get(artist_id=artist)

        try:
            results = data['response']['artist']
        except KeyError, error:
            print '%s: No data for artist %s %s' % (error, artist.name, artist.artist_id)
            continue

        try:
            echonest_response = results
            genres = results['genres']
            spotify_id = results['foreign_ids'][0]['foreign_id']
            familiarity = results['familiarity']
            hotttnesss = results['hotttnesss']
            years_active = results['years_active']
            location = results['artist_location']
            discovery = results['discovery']

        except KeyError, error:
            print 'An error has occured %s' % error
            pass

        artist.echonest_response = echonest_response
        artist.genres = genres
        artist.spotify_id = spotify_id
        artist.familiarity = familiarity
        artist.hotttnesss = hotttnesss
        artist.years_active = years_active
        artist.location = location
        artist.discovery = discovery
        artist.save()

        time.sleep(2)


def main():

    # connect to psql database: songick
    #create_tables()

    # retrieve venue ids from file: venues_2016.txt
    #venue_ids = get_venues()

    # retrieve artist ids where term1 is null
    #artist_ids = get_artists()

    # update venue data from songkick
    #update_venues(venue_ids)

    # update event data by venue from songkick
    #update_events(venue_ids)

    # update artist data (genre) from echonest
    #update_artists(artist_ids)

    # close connection to database
    #psql_db.close()


if __name__ == '__main__':
    main()
