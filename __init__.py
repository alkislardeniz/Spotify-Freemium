import sys

from selenium import webdriver

from freemiumSpotify.FreemiumSpotify import *


def main(spotify_playlist_url):
    driver = webdriver.Firefox()
    fs = FreemiumSpotify(spotify_playlist_url, driver)
    fs.retrieve_playlist_from_spotify()
    fs.find_and_download_mp3()
    driver.close()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Please give a Spotify playlist url as an argument!")
