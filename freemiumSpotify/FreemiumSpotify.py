from __future__ import unicode_literals

from os import path, getcwd
from pathlib import Path

import youtube_dl
from selenium.webdriver.common.keys import Keys

from freemiumSpotify.LogWriter import *


class FreemiumSpotify:
    SPOTIFY_PLAYLIST_LOAD_LIMIT = 100

    YES_MARK = "Y"
    NO_MARK = "N"
    FAIL_MARK = "F"

    def __init__(self, spotify_playlist_url, driver):
        self.spotify_playlist_url = spotify_playlist_url

        self.playlist_id = spotify_playlist_url[spotify_playlist_url.rindex('/') + 1:]

        self.playlist_file_name = getcwd() + "/" + self.playlist_id + "/" + "playlist.txt"
        self.playlist_download_log = getcwd() + "/" + self.playlist_id + "/" + "download_status.txt"
        self.driver = driver

    def create_download_directory(self, path):
        p = Path(path)
        p.mkdir(exist_ok=True)

    def retrieve_playlist_from_spotify(self):
        song_names_and_artists = []
        if not path.exists(self.playlist_file_name):
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.get(self.spotify_playlist_url)

            playlist_size = int(self.driver.find_element_by_css_selector(
                ".TrackListHeader__text-silence.TrackListHeader__entity-additional-info").text.split()[0])

            self.create_download_directory(self.playlist_id)

            if playlist_size > self.SPOTIFY_PLAYLIST_LOAD_LIMIT:
                for i in range(playlist_size * 2):
                    self.driver.find_element_by_css_selector("body").send_keys(Keys.TAB)

            song_names = self.driver.find_elements_by_css_selector(".tracklist-name.ellipsis-one-line")
            song_artists = self.driver.find_elements_by_css_selector(".TrackListRow__artists.ellipsis-one-line")

            playlist_file = open(self.playlist_file_name, 'w')

            playlist_download_log = open(self.playlist_download_log, 'w')
            for i in range(playlist_size):
                playlist_file.write(song_names[i].text.lower() + " " + song_artists[i].text.lower() + "\n")
                playlist_download_log.write(self.NO_MARK + "\n")
                song_names_and_artists.append(song_names[i].text.lower() + " " + song_artists[i].text.lower())

            playlist_file.close()
            playlist_download_log.close()
            self.driver.close()
        else:
            playlist_file = open(self.playlist_file_name, 'r')
            for line in playlist_file:
                song_names_and_artists.append(line)
            playlist_file.close()

        return song_names_and_artists

    def find_mp3_url_from_youtube(self, index, song_names_and_artists):
        self.driver.switch_to.window(self.driver.window_handles[0])
        youtube_search_bar = self.driver.find_element_by_name("search_query")
        youtube_search_bar.clear()
        youtube_search_bar.send_keys(song_names_and_artists[index])
        youtube_search_button = self.driver.find_element_by_id("search-icon-legacy")
        youtube_search_button.click()

        return self.driver.find_element_by_id("video-title").get_property("href")

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
            LogWriter.write_to_log_file_index(index, self.YES_MARK, self.playlist_download_log)
        except Exception:
            LogWriter.write_to_log_file_index(index, self.FAIL_MARK, self.playlist_download_log)

    def find_and_download_mp3(self, song_names_and_artists):
        download_length = len(song_names_and_artists)
        while True:
            any_download = False
            for i in range(download_length):
                print(i + 1, "/", len(song_names_and_artists))
                if LogWriter.read_from_log_file_index(i, self.playlist_download_log) != self.YES_MARK:
                    video_url = self.find_mp3_url_from_youtube(i, song_names_and_artists)
                    self.download_mp3_from_url(video_url, i)
                    any_download = any_download or True
                else:
                    any_download = any_download or False
            if not any_download:
                break
