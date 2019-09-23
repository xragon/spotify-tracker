# spotify-tracker
Retrieves discover weekly playlist and records it to a database

Makes use of https://github.com/plamere/spotipy


# ToDo
- include a date and unique identifer for the play list so we know which tracks were from which week (1)
- provide a refresh function to allow a manual run that will clear out any entries for the week from the DB and then repopulate it
- provide error notification process as this is meant to run without supervision

1. The playlist ID does not change week to week. Spotify just clear the existing playlist and add the new tracks. So a customer identifier will need to be created.