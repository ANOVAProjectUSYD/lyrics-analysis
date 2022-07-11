import io
import requests
import urllib.parse
from bs4 import BeautifulSoup

from search import *  # other Python file with functions

######################################################################
########### Main file to run everything #############################
#####################################################################

# Constants
base = "https://api.genius.com"
client_access_token = "-q1tRGBZMEOk6JewZCC_KWZBxyFSg9nccGlX11Cb3MxpGpzWG4FBSJIXCJS33D3x"


def connect_lyrics(song_id):
    '''Constructs the path of song lyrics.'''
    url = "songs/{}".format(song_id)
    data = get_json(url)

    # Gets the path of song lyrics
    path = data['response']['song']['path']

    return path


def retrieve_lyrics(song_id, song_title):
    '''Retrieves lyrics from html page.'''
    path = connect_lyrics(song_id)

    URL = "http://genius.com" + path
    page = requests.get(URL)

    # Extract the page's HTML as a string
    html = BeautifulSoup(page.text, "html.parser")

    # Scrape the song lyrics from the HTML
    lyrics_div = html.find(
        "div", class_=lambda value: value and value.startswith("Lyrics__Container"))
    if lyrics_div:
        lyrics = lyrics_div.contents
        return song_title, lyrics
    else:
        return song_title, None


def get_song_id(artist_id):
    '''Get all the song id from an artist.'''
    current_page = 1
    next_page = True
    songs = []  # to store final song ids

    while next_page:
        path = "artists/{}/songs/".format(artist_id)
        params = {'page': current_page}  # the current page
        data = get_json(path=path, params=params)  # get json of songs

        page_songs = data['response']['songs']
        if page_songs:
            # Add all the songs of current page
            songs += page_songs
            # Increment current_page value for next loop
            current_page += 1
            print("Page {} finished scraping".format(current_page))
            # If you don't wanna wait too long to scrape, un-comment this
            # if current_page == 2:
            #     break

        else:
            # If page_songs is empty, quit
            next_page = False

    print("Song id were scraped from {} pages".format(current_page))

    # Get all the song ids, excluding not-primary-artist songs.
    songs = [(song["id"], song["title"]) for song in songs
             if song["primary_artist"]["id"] == artist_id]

    return songs


def get_song_information(song_ids):
    '''Retrieve meta data about a song.'''
    # initialize a dictionary.
    song_list = {}
    print("Scraping song information")
    for i, song_id in enumerate(song_ids):
        print("id:" + str(song_id) + " start. ->")

        path = "songs/{}".format(song_id)
        data = get_json(path=path)["response"]["song"]

        song_list.update({
            i: {
                "title": data["title"],
                "album": data["album"]["name"] if data["album"] else "<single>",
                "release_date": data["release_date"] if data["release_date"] else "unidentified",
                "featured_artists":
                [feat["name"] if data["featured_artists"]
                    else "" for feat in data["featured_artists"]],
                "producer_artists":
                [feat["name"] if data["producer_artists"]
                    else "" for feat in data["producer_artists"]],
                "writer_artists":
                [feat["name"] if data["writer_artists"]
                    else "" for feat in data["writer_artists"]],
                "genius_track_id": song_id,
                "genius_album_id": data["album"]["id"] if data["album"] else "none"}
        })

        print("-> id:" + str(song_id) + " is finished. \n")
    return song_list


def main():
    # Example searches
    artist_name = "Wolf Alice"
    artist_id = 326078  # Wolf Alice

    # Grabs all song id's from artist
    songs_ids_titles = get_song_id(artist_id)

    # Get meta information about songs
    #song_list = get_song_information(songs_ids)

    # Scrape lyrics from the songs

    unwritten = 0
    with io.open('lyrics.html', mode='w', encoding='utf-8') as out:
        style = "@media print {"\
                "    .pagebreak { page-break-before: always; } /* page-break-after works, as well */"\
                "}"
        out.write(
            f'<html><head><title>{artist_name}</title><style>{style}</style></head><body>\n')
        for song_id_title in songs_ids_titles:
            song_title, lyrics = retrieve_lyrics(*song_id_title)
            if lyrics:
                out.write(f'<h2>{song_title}</h2>\n')
                for line in lyrics:
                    try:
                        out.write(str(line) + '\n')
                    except Exception as e:
                        print(e)
                        unwritten += 1
                out.write('\n<div class="pagebreak"/>\n')
                out.flush()
            else:
                unwritten += 1
        out.write('</body></html>\n')

    print(f"Could not write {unwritten} songs")

    # Gets information regarding the artist themself
    # followers = search_artist(artist_id)

    # Shows some random songs from arist and lyrics
    # search(term)


if __name__ == "__main__":
    main()
