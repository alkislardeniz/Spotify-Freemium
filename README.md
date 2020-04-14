# Spotify Freemium

<img src="https://raw.githubusercontent.com/alkislardeniz/freemium-spotify/master/sf.png" height="50%" width="50%">

<h1>What's that?</h1>
<p>Spotify Freemium is a simple program to download any publicly available Spotify playlist from YouTube. To get rid of any <b>API usage</b> both for <a href="https://developer.spotify.com/documentation/web-api/reference/playlists/get-playlists-tracks/">Spotify</a> and <a href="https://developers.google.com/youtube/v3/docs/search/list/">YouTube</a>, Selenium is used during fetching a playlist from Spotify and finding an alternative download URL from YouTube. It downloads the video as mp3 format by using the youtube-dl library. So the source code is really clean.</p>

<h2>Prerequisites</h2>
<p>To download dependencies(selenium, urllib3 and youtube-dl) of the project, you can use the following command: </p>

```
pip install -r requirements.txt
```
<b>Please don't forget to install a Selenium driver for your preferred browser.</b>

<h2>Running</h2>
<p>Use the following command to run the program: </p>

```
python __init__.py <SPOTIFY_PLAYLIST_URL> <BROWSER_TYPE>
```
Browser types are Chrome, Firefox, Opera and Safari. 

<b>Example call:</b>
```
python __init__.py https://open.spotify.com/playlist/7Jw2ZFk6NKVwXrW8MmOeGg chrome
```
<p>If there is an update in your playlist(a song was added and the number of songs in your playlist was increased), you can call the program again and it will download the newly added songs in your playlist.</p>
