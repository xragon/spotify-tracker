import sys
import spotipy
import spotipy.util as util
import psycopg2
from datetime import datetime, timedelta
import configparser



config = configparser.ConfigParser()
config.read('config.ini')
user_id = str(config['user']['id'])
db_name = config['database']['name']
db_user = config['database']['user']

db_connection = 'dbname={0} user={1}'.format(db_name,db_user)

conn = psycopg2.connect(db_connection)
cur = conn.cursor()

scope = 'user-library-read playlist-read-private'

token = util.prompt_for_user_token(user_id, scope)

def get_playlist_date(today):
    monday = today - timedelta(days=today.weekday())
    return monday.date()

def show_tracks(tracks):
    for item in tracks['items']:
        track = item['track']
        track_text = '{id} - {artist} - {album} - {title}'.format(
            id=track['id'], artist=track['artists'][0]['name'], album=track['album']['name'], title=track['name']
        )
        print(track_text)

def save_playlist():
    # playlist_date = get_playlist_date(datetime.today())
    playlist_date = '2019-04-04'

    cur.execute('SELECT id FROM discover_weekly_playlists WHERE CAST(dt AS DATE) = %s', playlist_date)
    playlist_id = cur.fetchone()

    print(playlist_id)

    # cur.execute('INSERT INTO discover_weekly_tracks (track_id, track_artist, track_album, track_title) VALUES (%s,%s,%s,%s)', 
    #     (track['id'], track['artists'][0]['name'], track['album']['name'], track['name']))

def main():
    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.current_user_playlists()
        for playlist in playlists['items']:
            if playlist['name'] == 'Discover Weekly':
                results = sp.user_playlist(user_id, playlist['id'],
                    fields="tracks")
                print(results)
                tracks = results['tracks']
                show_tracks(tracks)
                # while tracks['next']:
                #     tracks = sp.next(tracks)
                #     show_tracks(tracks)
    else:
        print("Can't get token for", user_id)

# main()
save_playlist()

conn.commit()
cur.close()
conn.close()
