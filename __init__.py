import sys

from selenium import webdriver

from freemiumSpotify.FreemiumSpotify import *


def create_driver(type):
    if type.lower() == "chrome":
        return webdriver.Chrome()
    elif type.lower() == "firefox":
        return webdriver.Firefox()
    elif type.lower == "opera":
        return webdriver.Opera()
    elif type.lower == "safari":
        return webdriver.Safari()
    else:
        return None


def main(spotify_playlist_url, type):
    driver = create_driver(type)
    if driver is not None:
        fs = FreemiumSpotify(spotify_playlist_url, driver)
        fs.retrieve_playlist_from_spotify()
        fs.find_and_download_mp3()
        driver.close()
    else:
        print("Browser types are Chrome, Firefox, Opera and Safari.")


if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("Valid call format: python __init__ <PLAYLIST_URL> <BROWSER_TYPE>")
