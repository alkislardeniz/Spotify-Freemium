from selenium import webdriver

from freemiumSpotify.FreemiumSpotify import *


def main():
    spotify_playlist_url = "https://open.spotify.com/playlist/7Jw2ZFk6NKVwXrW8MmOeGg"

    driver = webdriver.Firefox()
    fs = FreemiumSpotify(spotify_playlist_url, driver)
    fs.retrieve_playlist_from_spotify()
    fs.find_and_download_mp3()
    driver.close()


if __name__ == "__main__":
    main()
