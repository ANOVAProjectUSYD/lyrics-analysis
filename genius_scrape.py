import requests
import urllib.request
import urllib.parse
import json
from bs4 import BeautifulSoup


def search(term):
    '''Search Genius API.'''
    base = "https://api.genius.com/"
    search = "search?q="
    query = base + search + urllib.parse.quote(term)
    request = urllib.request.Request(query)
    client_access_token = "-q1tRGBZMEOk6JewZCC_KWZBxyFSg9nccGlX11Cb3MxpGpzWG4FBSJIXCJS33D3x"
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
    # get url of song lyrics and query for it
    URL = item['result']['url']
    print(URL)
    page = requests.get(URL)
    html = BeautifulSoup(page.text, "html.parser") # extract the page's HTML as a string
    # Scrape the song lyrics from the HTML
    lyrics = html.find("div", class_="lyrics").get_text()
    print(lyrics)


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
    print(data.keys())
    # TODO extract information


def main():
    # example searches
    term = 'Kanye West'
    artist_id = 72
    #search_artist(artist_id)
    search(term)



if __name__ == "__main__":
    main()
