import sys
import spotipy
import spotipy.util as util
import psycopg2

conn = psycopg2.connect('dbname= user=')
cur = conn.cursor()

scope = 'user-library-read playlist-read-private'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()

token = util.prompt_for_user_token(username, scope)

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        track_text = '{id} - {artist} - {album} - {title}'.format(
            id=track['id'], artist=track['artists'][0]['name'], album=track['album']['name'], title=track['name']
        )
        print(track_text)

        cur.execute('INSERT INTO discover_weekly_tracks (track_id, track_artist, track_album, track_title) VALUES (%s,%s,%s,%s)', 
        (track['id'], track['artists'][0]['name'], track['album']['name'], track['name']))

if token:
    sp = spotipy.Spotify(auth=token)
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:

        if playlist['name'] == 'Discover Weekly':
            results = sp.user_playlist(username, playlist['id'],
                fields="tracks,next")
            tracks = results['tracks']
            show_tracks(tracks)
            while tracks['next']:
                tracks = sp.next(tracks)
                show_tracks(tracks)
else:
    print("Can't get token for", username)

conn.commit()
cur.close()
conn.close()
