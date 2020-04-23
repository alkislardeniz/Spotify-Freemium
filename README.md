# Spotify Freemium

<img src="https://raw.githubusercontent.com/alkislardeniz/freemium-spotify/master/sf.png" height="50%" width="50%">

<h1>What's that?</h1>
<p>Spotify Freemium is a simple program to download any publicly available Spotify playlist from YouTube. To get rid of <b>API usage</b> for <a href="https://developer.spotify.com/documentation/web-api/reference/playlists/get-playlists-tracks/">Spotify</a>, Selenium is used. After fetching the playlist from Spotify, it finds an alternative download URL from YouTube and downloads the video as mp3 format by using the youtube-dl library. So the source code is really clean.</p>

<h2>Prerequisites</h2>
<p>To download dependencies of the project, you can use the following command: </p>

```
pip install -r requirements.txt
```
<b>Please don't forget to install a Selenium driver for your preferred browser.</b>

<h2>Usage</h2>
<p>Use the following command to run the program: </p>

```
python __init__.py <SPOTIFY_PLAYLIST_URL> <BROWSER_TYPE>
```
Browser types are Chrome, Firefox, Opera and Safari. 

<b>Example call:</b>
```
python __init__.py https://open.spotify.com/playlist/7Jw2ZFk6NKVwXrW8MmOeGg chrome
```
<p>If there is an update in your playlist, you can call the program again and it will only download the newly added songs.</p>
