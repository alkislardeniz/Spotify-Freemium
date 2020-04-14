# Spotify Freemium

<img src="https://raw.githubusercontent.com/alkislardeniz/freemium-spotify/master/sf.png" height="50%" width="50%">

<h1>What's that?</h1>
<p>Spotify Freemium is a simple program to download any publicly available Spotify playlist from YouTube. To get rid of any <b>API usage</b> both for Spotify and YouTube, Selenium is used during fetching a playlist from Spotify and finding an alternative download url from YouTube. It downloads the video as mp3 format by using the youtube-dl library. So the source code is really simple by the help of Selenium and youtube-dl.</p>

<h2>Prerequisites</h2>
<p>To download dependencies(selenium, urllib3 and youtube-dl) of the project, you can use the following command: </p>

```
pip install -r requirements.txt
```

<h2>Running</h2>
<p>Use the following command to run the program: </p>

```
python __init__.py <SPOTIFY_PLAYLIST_URL>
```
<p>If there is an update in your playlist(a song was added and the number of songs in your playlist was increased), you can call the program again and it will download the newly added songs in your playlist.</p>
