from models import Venue, Event, Artist, Performance
from collections import Counter

import csv
import os


SONGKICK = 'w3SLl77oVdu8etaS'
ECHONEST = 'Y3MVATIRX6THKQGGY'

def get_venues():

    songkick_directory = os.path.dirname(__file__)
    venues_master = os.path.join(songkick_directory, 'venues_2016.txt')

    venue_data = []
    f = open(venues_master, 'rb')
    try:
        reader = csv.reader(f)
        for row in reader:
            venue_data.append(int(row[0]))
    except IndexError:
        pass
    finally:
        f.close()
    return venue_data

def get_artists():

    selection = Artist.select().where(Artist.echonest_response.is_null(True))
    artist_list = [artist.artist_id for artist in selection]
    return artist_list


def genre_dictionary():

    genre_map = {
    	'rock': ['rock', 'psychedelic', 'grunge', 'post-grunge', 'experimental rock',
    		'industrial', 'industrial rock', 'jam band', 'hard rock',
    		'psychedelic rock', 'southern rock', 'rock \'n roll', 'instrumental rock', 'acoustic rock',
    		'classic rock', 'glam rock', 'space rock', 'stoner rock', 'kraut rock', 'krautrock',
    		'no wave', 'progressive rock', 'roots rock', 'alternative', 'alternative rock',
    		'modern rock', 'soft rock', 'american rock', 'shock rock', 'melodic rock',
    		'70s rock', '90s rock'],
    	'pop': ['pop', 'alternative pop', 'power pop', 'pop rock', 'emo', 'pop punk', 'boy band',
    		'kpop, j pop', 'teen pop', '80s', '90s', '70s', 'sunshine pop', 'surf music',
    		'german pop', 'russian pop', 'operatic pop', 'vocal pop', 'folk-pop', '00s',
    		'60s', 'british pop'],
    	'folk': ['folk', 'singer-songwriter', 'folk rock', 'traditional folk', 'modern folk',
    		'psychedelic folk', 'string band', 'americana', 'bluegrass', 'contemporary folk',
    		'alternative folk', 'pagan folk', 'urban folk'],
    	'punk': ['punk', 'ska', 'ska punk', 'skate punk', 'japanoise', 'hardcore punk',
    		'garage punk', 'street punk', 'oi', 'oi!', 'glam punk', 'art punk', 'crust punk',
    		'punk rock', 'new york hardcore', 'crossover thrash', 'post-hardcore', 'screamo',
    		'anarcho-punk', 'peace punk', 'melodic punk', 'swedish punk', 'folk punk',
    		'riot grrrl', 'crust', 'street punk', 'mod revival', 'melodic hardcore'],
    	'electronic': ['electronic', 'house', 'dance', 'dubstep', 'techno', 'electro', 'disco', 'ambient',
    		'electronica', 'lounge', 'edm', 'electro house', 'drone', 'downtempo', 'grime',
    		'deep house', 'drum and bass', 'trance', 'electropop', 'breakbeat', 'minimal',
    		'break', 'trip hop', 'acid jazz', 'big beat', 'bass music', 'indietronica',
    		'hardstyle', 'glitch', 'tech house', 'new rave', 'scratch', 'swedish house', 'jungle',
    		'progressive house', 'disco house', 'remix', 'futurepop', 'club',
    		'intelligent dance music', 'glitch hop', 'ebm', 'folktronica',
    		'birmingham techno', 'acid house', 'post-industrial', 'minimal techno', 'nu disco',
    		'uk garage', 'jungle music', 'bastard pop', 'fidget house', 'electroclash',
    		'space disco', 'alternative dance', 'dance music', 'italian disco', 'microhouse',
    		'detroit techno', 'french house', 'hardcore techno'],
    	'jazz': ['jazz', 'modern jazz', 'smooth jazz', 'jazz funk', 'jazz fusion', 'cool jazz', 'bebop',
    		'crossover jazz', 'avant-garde jazz', 'free jazz', 'new orleans jazz', 'jazz vocal',
    		'hard bop', 'west coast jazz', 'soul jazz', 'bossa nova', 'contemporary jazz',
    		'jazz rock'],
    	'metal': ['metal', 'death metal', 'black metal', 'heavy metal', 'thrash metal',
    		'progressive metal', 'metalcore', 'power metal', 'sludge metal', 'gothic metal',
    		'viking metal', 'doom metal', 'technical death metal', 'grindcore', 'hardcore', 'sludge',
    		'folk metal', 'nu metal', 'pagan metal', 'stoner metal', 'melodic death metal',
    		'speed metal', 'symphonic metal', 'technical thrash metal', 'industrial metal',
    		'deathgrind', 'alternative metal'],
    	'hip hop': ['hip hop', 'rap', 'underground hip hop', 'alternative rap', 'southern rap',
    		'west coast rap', 'independent hip hop', 'hardcore hip hop;', 'gangster rap',
    		'old school hip hop', 'east coast hip hop', 'alternative hip hop', 'dirty south rap',
    		'southern hip hop', 'christian rap', 'underground rap', 'pop rap',
    		'instrumental hip hop', 'jazz hip hop', 'hardcore rap', 'reggaeton', 'latin rap'],
    	'indie': ['indie', 'indie rock', 'indie pop', 'noise pop', 'chillwave', 'nu gaze', 'chamber pop',
    		'synthpop', 'dream pop', 'new wave', 'art rock', 'madchester',
    		'math rock', 'freak folk', 'dance-punk', 'canadian indie', 'noise rock',
    		'post-punk', 'garage rock', 'lo-fi', 'baroque pop', 'jangle pop', 'post rock', 'post-rock',
    		'sadcore', 'c86', 'noise', 'shoegaze', 'baroque', 'experimental', 'indie folk',
    		'canadian indie', 'twee pop', 'dark ambient', 'avant-garde', 'dance rock'],
    	'blues': ['blues', 'blues-rock', 'chicago blues', 'contemporary blues', 'desert blues',
    		'modern blues', 'delta blues', 'traditional blues', 'memphis blues', 'acoustic blues',
    		'texas blues', 'country blues', 'louisiana blues', 'swamp blues', 'soul blues'],
    	'soul': ['soul', 'funk', 'motown', 'gospel', 'neo soul', 'chicago soul', 'soul blues',
    		'southern soul', 'northern soul', 'jazz blues', 'memphis soul', 'doo-wop',
    		'soul music', 'nu-soul'],
    	'country': ['country', 'alternative country', 'western swing', 'honky tonk',
    		'country music', 'traditional country', 'texas country'],
    	'r&b': ['r&b', 'contemporary r&b'],
    	'classical': ['classical', 'symphony', 'opera', 'chamber music', 'classical period',
    		'renaissance', 'contemporary classical music'],
    	'reggae': ['reggae', 'dub', 'dancehall', 'reggae fusion', 'roots', 'roots reggae',
    		'ragga jungle', 'reggae rock'],
    	'world': ['world', 'world music', 'fusion', 'spiritual', 'afrobeat', 'christian', 'celtic',
    		'new age', 'indian classical', 'tango', 'rumba', 'flamenco', 'goa trance', 'samba',
    		'balkan beat', 'world fusion', 'gypsy jazz', 'gypsy music', 'island music',
    		'balkan brass', 'celtic rock', 'mariachi', 'pinoy rock', 'persian pop'],
    	'latin': ['latin', 'latin jazz', 'latin alternative', 'banda', 'cumbia', 'norteno'],
    	'comedy': ['comedy', 'stand-up comedy'],
    	'other': ['rockabilly', 'easy listening', 'psychobilly', 'swing', 'gothic', 'vocal jazz',
    		'cabaret', 'soundtrack', 'romantic', 'nintendocore', 'aggrotech', 'jrock',
    		'visual kei', 'psychedelic dub', 'psychedelia', 'pop underground', 'instrumental',
    		'texas music', 'old school', 'psychedelic chill']
    	}

    return genre_map



def get_terms():

    genres = []
    artist = Artist.select()
    genre_list = [a.genres for a in artist if a.genres]
    for l in genre_list:
        for i in l:
            genres.append(i['name'])
    term_count = Counter(genres)
    return term_count


def update_term():

    term_counts = get_terms()
    artist = Artist.select()
    for a in artist:
        temp_terms = {}
        if a.genres:
            for g in a.genres:
                if g['name'] in term_counts:
                    temp_terms[g['name']] = term_counts[g['name']]
                    #temp_terms.append({g['name']: term_counts[g['name']]})
                    #print g['name'], term_counts[g['name']]
            top_term = max(temp_terms.iterkeys(), key = (lambda k: temp_terms[k]))
            a.term1 = top_term
            a.save()
