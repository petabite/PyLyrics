# PyLyrics
#### gets lyrics for song playing in spotify

#### how to use:
---

spotify must be open in order for this to work


run `python pylyrics.py` for CLI mode


run `python pylyricsgui.py` for GUI mode

#### how it works
---
1. get the title of the spotify window, which contains the song and artist
2. create a search query in the format: song+artist(replacing all spaces with '+')
3. plug in the query to genius search api url
4. find lyrics url from response
5. send get request to lyrics url
6. scrape lyrics from html
7. display the lyrics!
