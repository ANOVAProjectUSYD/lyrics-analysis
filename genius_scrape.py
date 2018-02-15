import requests
import urllib.request
import urllib.parse
import json
from bs4 import BeautifulSoup

# Constants
base = "https://api.genius.com"
client_access_token = "-q1tRGBZMEOk6JewZCC_KWZBxyFSg9nccGlX11Cb3MxpGpzWG4FBSJIXCJS33D3x"


def search(term):
    '''Search Genius API.'''

    search = "search?q="
    query = base + search + urllib.parse.quote(term)
    request = urllib.request.Request(query)

    request.add_header("Authorization", "Bearer " + client_access_token)
    request.add_header("User-Agent", "")

    response = urllib.request.urlopen(request, timeout=3)
    raw = response.read()
    data = json.loads(raw)['response']['hits']

    for item in data:
        # print the artist and title of each result
        print(item['result']['primary_artist']['name']
              + ': ' + item['result']['title'])

        get_lyrics(item)


def get_lyrics(item):
    '''Grabs the lyrics of the song via using the song's URL'''
    # Get url of song lyrics and query for it
    URL = item['result']['url']
    print(URL)
    page = requests.get(URL)
    html = BeautifulSoup(page.text, "html.parser") # extract the page's HTML as a string
    # Scrape the song lyrics from the HTML
    lyrics = html.find("div", class_="lyrics").get_text()
    print(lyrics)


def get_json(path, params=None, headers=None):
    '''Send request and get response in json format.'''

    # Generate request URL
    requrl = '/'.join([base, path])
    token = "Bearer {}".format(client_access_token)
    if headers:
        headers['Authorization'] = token
    else:
        headers = {"Authorization": token}

    # Get response object from querying genius api
    response = requests.get(url=requrl, params=params, headers=headers)
    response.raise_for_status()

    return response.json()


def get_song_id(artist_id):
    '''Get all the song id from an artist.'''
    current_page = 1
    next_page = True
    songs = [] # to store final song ids

    while next_page:

        path = "artists/{}/songs/".format(artist_id)
        params = {'page': current_page} # the current page
        data = get_json(path=path, params=params) # get json of songs

        page_songs = data['response']['songs']
        if page_songs:
            # Add all the songs of current page
            songs += page_songs
            # Increment current_page value for next loop
            current_page += 1
            print("Page {} finished scraping".format(current_page))
            if current_page == 2: #don't wanna wait too long so needa remove
                break
        else:
            # If page_songs is empty, quit
            next_page = False

    print("Song id were scraped from {} pages".format(current_page))

    # Get all the song ids, excluding not-primary-artist songs.
    songs = [song["id"] for song in songs
            if song["primary_artist"]["id"] == artist_id]

    return songs


def search_artist(artist_id):
    '''Search on Genius API via Artist ID.'''
    base = "https://api.genius.com/"
    search = "artists/"
    query = base + search + str(artist_id)
    request = urllib.request.Request(query)
    client_access_token = "-q1tRGBZMEOk6JewZCC_KWZBxyFSg9nccGlX11Cb3MxpGpzWG4FBSJIXCJS33D3x"
    request.add_header("Authorization", "Bearer " + client_access_token)
    request.add_header("User-Agent", "")

    response = urllib.request.urlopen(request, timeout=3)
    raw = response.read()
    data = json.loads(raw)['response']['artist']
    # Lots of information we can scrape regarding the artist, check keys
    return data["followers_count"] # number of followers


def get_song_information(song_ids):
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
                [feat["name"] if data["featured_artists"] else "" for feat in data["featured_artists"]],
            "producer_artists":
                [feat["name"] if data["producer_artists"] else "" for feat in data["producer_artists"]],
            "writer_artists":
                [feat["name"] if data["writer_artists"] else "" for feat in data["writer_artists"]],
            "genius_track_id": song_id,
            "genius_album_id": data["album"]["id"] if data["album"] else "none"}
        })

        print("-> id:" + str(song_id) + " is finished. \n")
    return song_list


def main():
    # example searches
    term = 'Kanye West'
    artist_id = 72

    # Gets information regarding the artist themself
    #followers = search_artist(artist_id)

    # Shows some random songs from arist and lyrics
    #search(term)

    songs_ids = get_song_id(72)
    #print(songs_ids)

    song_list = get_song_information(songs_ids)
    #print(song_list)


if __name__ == "__main__":
    main()
