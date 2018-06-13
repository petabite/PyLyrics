import requests
from bs4 import BeautifulSoup
import ctypes

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible

def get_song_info():
    titles = []
    def foreach_window(hwnd, lParam):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            titles.append(buff.value)
        return True
    EnumWindows(EnumWindowsProc(foreach_window), 0)
    for item in titles:
        if '-' in item and 'Google' not in item and 'python' not in item and 'cmd' not in item:
            return item

def create_search_query(artist, song):
    new_artist_string = artist.replace(' ', '+')
    new_song_string = song.replace(' ', '+')
    new_song_string = new_song_string.replace('&', 'and')
    return new_song_string + '%20' + new_artist_string

def create_lyrics_url(search_query):
    search_url = 'https://genius.com/api/search/multi?per_page=2&q=' + search_query
    # print(search_url)
    search_request = requests.get(search_url)
    lyrics_url = search_request.json()['response']['sections'][0]['hits'][0]['result']['url']
    return lyrics_url

def get_lyrics(url):
    lyrics_html = requests.get(url)
    soup = BeautifulSoup(lyrics_html.content, "html.parser")
    lyrics = soup.find('div', 'lyrics').get_text()
    return lyrics

if __name__ == '__main__':
    song_string = get_song_info().split(' - ')
    artist = song_string[0]
    song = song_string[1]
    query = create_search_query(artist,song)
    lyrics_url = create_lyrics_url(query)
    lyrics = get_lyrics(lyrics_url)
    print('='*10)
    print('PYLYRICS')
    print('='*10)
    print('Finding lyrics for: ' + song + ' by ' + artist)
    print('Searching @ ' + lyrics_url)
    print('LYRICS: ')
    print(lyrics)
