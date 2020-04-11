from selenium import webdriver

from FreemiumSpotify import *


def main():
    spotify_playlist_url = "https://open.spotify.com/playlist/1gGDDJ70mCzp59JQnoKC0M"
    # spotify_playlist_url = "https://open.spotify.com/playlist/7Jw2ZFk6NKVwXrW8MmOeGg

    driver = webdriver.Firefox()
    fs = FreemiumSpotify(spotify_playlist_url, driver)

    driver.get("http://www.youtube.com")
    song_names_and_artists = fs.retrieve_playlist_from_spotify()
    fs.find_and_download_mp3(song_names_and_artists)
    driver.close()


if __name__ == "__main__":
    main()
