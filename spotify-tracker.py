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
        # print "   %d %32.32s %s" % (i, track['artists'][0]['name'], track['name'])
        # print(i, track['artists'][0]['name'], track['name'])
        track_text = '{id} - {artist} - {album} - {title}'.format(
            id=track['id'], artist=track['artists'][0]['name'], album=track['album']['name'], title=track['name']
        )
        print(track_text)

#         insert_sql = 'INSERT INTO discover_weekly_tracks (track_id, track_artist, track_album, track_title) VALUES ("{id}", "{artist}", "{album}", "{title}")'.format(
#             id=track['id'], artist=track['artists'][0]['name'], album=track['album']['name'], title=track['name'])


# cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",
# ...      (100, "abc'def"))

#         print(insert_sql)

        # cur.execute(insert_sql)

        cur.execute('INSERT INTO discover_weekly_tracks (track_id, track_artist, track_album, track_title) VALUES (%s,%s,%s,%s)', 
        (track['id'], track['artists'][0]['name'], track['album']['name'], track['name']))

if token:
    sp = spotipy.Spotify(auth=token)
    # playlists = sp.user_playlists(username)
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        # print(playlist['name'])
        if playlist['name'] == 'Discover Weekly':
            # print(playlist['name'])
            # print(playlist)
            # print('  total tracks', playlist['tracks']['total'])
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