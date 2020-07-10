#!/usr/local/bin/python3
import pylyrics
import tkinter as tk
from tkinter import font

# init tk window
root = tk.Tk()
root.title("PyLyrics")

default_font = font.nametofont("TkDefaultFont")
default_font.configure(size=12, family="courier")
# TODO: tkinter, use pylyrics logo


def refresh_window():
    pylyricsframe.destroy()
    create_window()


def create_window():
    global pylyricsframe
    pylyricsframe = tk.Frame(root)
    pylyricsframe.pack()
    searching_label = tk.Label(pylyricsframe)
    searching_label.pack()
    try:
        song, artist = pylyrics.get_song_info()
        searching_label.config(text="Finding lyrics for: " + song + " by " + artist)

        query = pylyrics.create_search_query(artist, song)
        lyrics_url = pylyrics.create_lyrics_url(query)
        search_url_label = tk.Label(pylyricsframe, text="Searching @ " + lyrics_url)
        search_url_label.pack()

        lyrics = pylyrics.get_lyrics(lyrics_url)
        lyrics_text = tk.Text(
            pylyricsframe, bg="#f0f0ed", padx=10, pady=10, relief=tk.FLAT, wrap=tk.WORD
        )
        lyrics_text.tag_configure("center", justify="center")
        lyrics_text.insert(tk.INSERT, lyrics)
        lyrics_text.tag_add("center", 1.0, "end")
        lyrics_text.config(state=tk.DISABLED)
        lyrics_text.pack()
    except:
        # print(e)
        searching_label.config(text="A song isn't playing right now")


# create frame and labels
title_label = tk.Label(root, text="PyLyrics", font=("courier", 30, "bold"))
title_label.pack()
refresh_button = tk.Button(root, text="Refresh", command=refresh_window)
refresh_button.pack()
create_window()

# run window
root.mainloop()
