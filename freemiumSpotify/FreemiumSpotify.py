import urllib.request
from os import path, getcwd
from pathlib import Path

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
        self.playlist_file_name = getcwd() + "/" + self.playlist_id + "/" + self.playlist_id + "_playlist.txt"
        self.playlist_download_log = getcwd() + "/" + self.playlist_id + "/" + self.playlist_id + "_download_status.txt"
        self.playlist_size = getcwd() + "/" + self.playlist_id + "/" + self.playlist_id + "_size.txt"
        self.driver = driver
        self.driver.get(self.spotify_playlist_url)

        self.song_names_and_artists = []

    def create_download_directory(self, path):
        p = Path(path)
        p.mkdir(exist_ok=True)

    def retrieve_playlist_from_spotify(self):
        playlist_size = int(self.driver.find_element_by_css_selector(
            ".TrackListHeader__text-silence.TrackListHeader__entity-additional-info").text.split()[0])
        prev_playlist_size = int(FileHandler.read_from_file_index(0, self.playlist_size)) if path.exists(
            self.playlist_size) else 0

        if playlist_size > self.SPOTIFY_PLAYLIST_LOAD_LIMIT and playlist_size > prev_playlist_size:
            for i in range(playlist_size * 2):
                self.driver.find_element_by_css_selector("body").send_keys(Keys.TAB)

        song_names = self.driver.find_elements_by_css_selector(".tracklist-name.ellipsis-one-line")
        song_artists = self.driver.find_elements_by_css_selector(".TrackListRow__artists.ellipsis-one-line")

        if not path.exists(self.playlist_size):
            self.create_download_directory(self.playlist_id)

            playlist_file = open(self.playlist_file_name, 'w')
            playlist_download_log = open(self.playlist_download_log, 'w')

            for i in range(playlist_size):
                playlist_file.write(song_names[i].text.lower() + " " + song_artists[i].text.lower() + "\n")
                playlist_download_log.write(self.NO_MARK + "\n")
                self.song_names_and_artists.append(song_names[i].text.lower() + " " + song_artists[i].text.lower())

            playlist_file.close()
            playlist_download_log.close()
        else:
            if prev_playlist_size < playlist_size:
                for i in range(prev_playlist_size, playlist_size):
                    newly_added_song = song_names[i].text.lower() + " " + song_artists[i].text.lower()
                    FileHandler.append_to_a_file(newly_added_song, self.playlist_file_name)
                    FileHandler.append_to_a_file(self.NO_MARK, self.playlist_download_log)

            playlist_file = open(self.playlist_file_name, 'r')
            for line in playlist_file:
                self.song_names_and_artists.append(line)
            playlist_file.close()

        size_file = open(self.playlist_size, "w")
        size_file.write(str(playlist_size))
        size_file.close()

        self.driver.close()

    def find_mp3_url_from_youtube(self, song_name_and_artist):
        query = urllib.parse.quote(song_name_and_artist)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        video = soup.find(attrs={'class': 'yt-uix-tile-link'})
        return 'https://www.youtube.com' + video['href']

    def download_mp3_from_url(self, video_url, index):
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
            FileHandler.write_to_file_index(index, self.YES_MARK, self.playlist_download_log)
        except Exception:
            FileHandler.write_to_file_index(index, self.FAIL_MARK, self.playlist_download_log)

    def find_and_download_mp3(self):
        download_length = len(self.song_names_and_artists)
        while True:
            any_download = False
            for i in range(download_length):
                if FileHandler.read_from_file_index(i, self.playlist_download_log) != self.YES_MARK:
                    print("Trying ", i + 1, "/", len(self.song_names_and_artists))
                    video_url = self.find_mp3_url_from_youtube(self.song_names_and_artists[i])
                    self.download_mp3_from_url(video_url, i)
                    any_download = any_download or True
                else:
                    print("Already downloaded ", i + 1, "/", len(self.song_names_and_artists))
                    any_download = any_download or False
            if not any_download:
                print("Downloaded all the playlist successfully!")
                break
