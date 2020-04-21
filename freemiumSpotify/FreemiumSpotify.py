import urllib.request
from os import path, getcwd

import youtube_dl
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

from freemiumSpotify.FileHandler import *


class FreemiumSpotify:
    SPOTIFY_PLAYLIST_LOAD_LIMIT = 100

    YES_MARK = "Y"
    NO_MARK = "N"
    FAIL_MARK = "F"

    def __init__(self, spotify_playlist_url, driver):
        self.spotify_playlist_url = spotify_playlist_url
        self.playlist_id = spotify_playlist_url[spotify_playlist_url.rindex('/') + 1:]
        self.log_file_name = getcwd() + "/" + self.playlist_id + "/" + self.playlist_id + "_download_log.pkl"
        self.driver = driver
        self.driver.get(self.spotify_playlist_url)

        self.playlist_download_status = {}
        if path.exists(self.log_file_name):
            self.playlist_download_status = FileHandler.load_obj(self.log_file_name)

    def retrieve_playlist_from_spotify(self):
        playlist_size = int(self.driver.find_element_by_css_selector(
            ".TrackListHeader__text-silence.TrackListHeader__entity-additional-info").text.split()[0])

        if playlist_size > self.SPOTIFY_PLAYLIST_LOAD_LIMIT:
            for i in range(playlist_size * 2):
                self.driver.find_element_by_css_selector("body").send_keys(Keys.TAB)

        song_names = self.driver.find_elements_by_css_selector(".tracklist-name.ellipsis-one-line")
        song_artists = self.driver.find_elements_by_css_selector(".TrackListRow__artists.ellipsis-one-line")

        if not path.exists(self.log_file_name):
            FileHandler.create_download_directory(self.playlist_id)

        for i in range(playlist_size):
            song_name_and_artist = song_names[i].text.lower() + " " + song_artists[i].text.lower()
            if song_name_and_artist not in self.playlist_download_status:
                self.playlist_download_status[song_name_and_artist] = self.NO_MARK

        self.driver.close()

    def find_mp3_url_from_youtube(self, song_name_and_artist):
        query = urllib.parse.quote(song_name_and_artist)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        video = soup.find(attrs={'class': 'yt-uix-tile-link'})
        return 'https://www.youtube.com' + video['href']

    def download_mp3_from_url(self, song, video_url):
        try:
            ydl_opts = {
                'writethumbnail': True,
                'format': 'bestaudio/best',
                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    },
                    {'key': 'EmbedThumbnail'}, {'key': 'FFmpegMetadata'}],
                'outtmpl': getcwd() + '/' + self.playlist_id + '/' + '%(title)s.%(ext)s',
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            self.playlist_download_status[song] = self.YES_MARK
        except Exception:
            self.playlist_download_status[song] = self.FAIL_MARK

        FileHandler.save_obj(self.playlist_download_status, self.log_file_name)

    def find_and_download_mp3(self):
        while True:
            i = 1
            any_download = False
            for song in self.playlist_download_status:
                if self.playlist_download_status[song] != self.YES_MARK:
                    print("Trying ", i, "/", len(self.playlist_download_status))
                    video_url = self.find_mp3_url_from_youtube(song)
                    self.download_mp3_from_url(song, video_url)
                    any_download = any_download or True
                else:
                    print("Already downloaded ", i, "/", len(self.playlist_download_status))
                    any_download = any_download or False
                i += 1
            if not any_download:
                print("Downloaded all the playlist successfully!")
                break
