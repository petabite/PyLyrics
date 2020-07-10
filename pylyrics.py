import requests
from bs4 import BeautifulSoup
import ctypes
from subprocess import Popen, PIPE
from sys import platform


def get_song_info():
    if platform == "darwin":
        # macOS

        script = """tell application "Spotify" to return (get name of current track) & " - " & (get artist of current track)"""
        p = Popen(["osascript", "-"], stdin=PIPE, stdout=PIPE)
        stdout, _ = p.communicate(script.encode("utf-8"))
        song_string = stdout.decode("utf-8").strip()
    elif platform == "win32":
        # Windows...
        EnumWindows = ctypes.windll.user32.EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(
            ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)
        )
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
        # code above not my code
        for item in titles:
            if (
                "-" in item
                and "Google" not in item
                and "python" not in item
                and "Calculator" not in item
            ):
                song_string = item
    song_string = song_string.split(" - ")
    artist = song_string[0]
    song = song_string[1]
    return artist, song


def create_search_query(artist, song):
    new_artist_string = artist.replace(" ", "+")
    new_song_string = song.replace(" ", "+")
    new_song_string = new_song_string.replace("&", "and")
    if "(" in new_song_string:
        start = new_song_string.find("(")
        end = new_song_string.find(")")
        to_be_replaced = new_song_string[start:end]
        new_song_string = new_song_string.replace(to_be_replaced, "")
    return new_song_string + "%20" + new_artist_string


def create_lyrics_url(search_query):
    search_url = "https://genius.com/api/search/multi?per_page=2&q=" + search_query
    # print(search_url)
    search_request = requests.get(search_url)
    lyrics_url = search_request.json()["response"]["sections"][0]["hits"][0]["result"][
        "url"
    ]
    return lyrics_url


def get_lyrics(url):
    lyrics_html = requests.get(url)
    soup = BeautifulSoup(lyrics_html.content, "html.parser")
    lyrics = soup.find("div", "lyrics").get_text()
    return lyrics


if __name__ == "__main__":
    song, artist = get_song_info()
    query = create_search_query(artist, song)
    lyrics_url = create_lyrics_url(query)
    lyrics = get_lyrics(lyrics_url)
    print("=" * 10)
    print("PYLYRICS")
    print("=" * 10)
    print("Finding lyrics for: " + song + " by " + artist)
    print("Searching @ " + lyrics_url)
    print("LYRICS: ")
    print(lyrics)
