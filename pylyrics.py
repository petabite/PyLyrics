import requests
from bs4 import BeautifulSoup
#
# spotify_req = requests.get('https://open.spotify.com')
# soup = BeautifulSoup(spotify_req.content, "html.parser")
# print(spotify_req.content)
# print(soup.title.string)

import ctypes

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible

titles = []
def foreach_window(hwnd, lParam):
    if IsWindowVisible(hwnd):
        length = GetWindowTextLength(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        GetWindowText(hwnd, buff, length + 1)
        titles.append(buff.value)
    return True
EnumWindows(EnumWindowsProc(foreach_window), 0)

# all code above this line is not my code

def get_song_info():
    for item in titles:
        if '-' in item and 'Google' not in item and 'python' not in item and 'cmd' not in item:
            return item

song_string= get_song_info().split(' - ')
artist = song_string[0]
song = song_string[1]
print(artist)
print(song)
def create_search_query(artist, song):
    new_artist_string = artist.replace(' ', '+')
    new_song_string = song.replace(' ', '+')
    # print(new_artist_string)
    return new_song_string + '%20' + new_artist_string
# create_search_query(artist,song)
search_url = 'https://genius.com/api/search/multi?per_page=2&q=' + create_search_query(artist,song)
print(search_url)
search_request = requests.get(search_url)
lyrics_url = search_request.json()['response']['sections'][0]['hits'][0]['result']['url']
# print(search_request.content)
# search_soup = BeautifulSoup(search_request.content, 'html.parser')
# print(search_soup.findAll('a'))

lyrics_html = requests.get(lyrics_url)
soup = BeautifulSoup(lyrics_html.content, "html.parser")
lyrics = soup.find('div', 'lyrics').get_text()
print(lyrics)
