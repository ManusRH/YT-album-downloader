print("\nInitiating...")

from urllib.request import urlopen
from pytube import YouTube
from pydub import AudioSegment
from bs4 import BeautifulSoup
import os
import os.path
import eyed3
import sys

print()

url = input("Paste url of playlist: ").strip(" ")
artist = input("Enter artist name: ")
album = input("Enter album name: ")

folder = "/".join(os.path.realpath(__file__).split("\\")[:-1]) + "/" + album + " by " + artist + "/"

if not os.path.exists(folder):
    os.makedirs(folder)

videos = []

print("loading playlist... \n")

while len(videos) == 0:
    html_page = urlopen(url)
    soup = BeautifulSoup(html_page, "lxml")
    for link in soup.findAll('a'):
        link = link.get('href')
        if link[1:8] == "watch?v" and "index=" in link and \
        "https://www.youtube.com" + str(link.strip("\n")[0:20]) not in videos:
            videos.append("https://www.youtube.com" + str(link.strip("\n")[0:20]))

n = 1

for link in videos:
    try:
        yt = YouTube(link)
    except:
        print("\nThe video is age retricted or unavailable and cannot be downloaded :(\n")
        continue

    print("Downloading:", yt.filename)

    for vid in yt.filter('mp4')[::-1]:
        if "1080p" in str(vid):
            video = yt.get('mp4', '1080p')
            break
        elif "720p" in str(vid):
            video = yt.get('mp4', '720p')
            break
        elif "480p" in str(vid):
            video = yt.get('mp4', '480p')
            break
        elif "360p" in str(vid):
            video = yt.get('mp4', '360p')
            break

    try:
        video
    except:
        for vid in yt.filter('flv')[::-1]:
            if "1080p" in str(vid):
                video = yt.get('flv', '1080p')
                break
            elif "720p" in str(vid):
                video = yt.get('flv', '720p')
                break
            elif "480p" in str(vid):
                video = yt.get('flv', '480p')
                break
            elif "360p" in str(vid):
                video = yt.get('flv', '360p')
                break

    yt.set_filename(str(n) + " - " + yt.filename)
    n += 1

    video.download(folder)

print()

for file in [f for f in os.listdir(folder) \
            if os.path.isfile(os.path.join(folder, f))]:
    print("Converting", '"'+file+'"', "to mp3...")
    AudioSegment.from_file(folder + file).export((folder+file)[:-3]+"mp3", format="mp3")
    os.remove(folder + file)

print()

for file in [f for f in os.listdir(folder) \
            if os.path.isfile(os.path.join(folder, f))]:
    aud = eyed3.load(folder + file)
    aud.tag.artist = u"{}".format(artist)
    aud.tag.album  = u"{}".format(album)
    print("Tack", file.split(" ")[0] + ":", file)
    aud.tag.title  = u"{}".format(input("Enter track title: "))
    aud.tag.track_num = int(file.split(" ")[0])
    aud.tag.save()

print("\nSuccess!")
