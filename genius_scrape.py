import requests
import urllib.request
import urllib.parse
import json

# Search Genius on any search term
def search(term):
    # Create Genuis API request
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
        # Print the artist and title of each result
        print(item['result']['primary_artist']['name']
              + ': ' + item['result']['title'])


# Seach Genuis on API artist id
def search_artist(artist_id):
    # Create Genuis API request
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
    # Example searches
    term = 'Kanye West'
    artist_id = 72
    search_artist(artist_id)
    search(term)


if __name__ == "__main__":
    main()
