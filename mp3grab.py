import requests
from bs4 import BeautifulSoup
import argparse
import urllib2


class MediaDownloader(object):
    SERVICE_NAME = None  # SERVICE_NAME = 'youtube'
    def __init__(self):
        pass

    def _get_mp3_list(self, url):
        raise NotImpementedError()

    def download(self, url, dir=None):
        raise NotImpementedError()


class YoutubeDownloader(MediaDownloader):
    def get_mp3_list(self):
        mp3_list = []
        mp3_list.append(self.url)
        return mp3_list

    def download(self, url,dir = None):
        self.url = url
        self.dir = dir
        source_html = requests.get(self.url).text
        soup = BeautifulSoup(source_html, 'html.parser')
        song_name = ''
        api_url = 'http://www.youtubeinmp3.com/fetch/?video='
        for x in soup.findAll('span', {'class': 'watch-title'}):
            song_name = str(x.get('title'))
        mp3file = urllib2.urlopen(api_url + self.get_mp3_list()[0])
        if self.dir == None:
            with open(song_name +'.mp3', 'wb') as output:
                output.write(mp3file.read())
        elif self.dir != None:
            with open(self.dir + song_name +'.mp3', 'wb') as output:
                output.write(mp3file.read())


class YoutubePlaylistDownloader(MediaDownloader):
    def get_mp3_list(self):

        mp3_list = []
        source_html = requests.get(self.url).text
        soup = BeautifulSoup(source_html, 'html.parser')
        for song_link in soup.find_all('a',{'class':'pl-video-title-link yt-uix-tile-link yt-uix-sessionlink  spf-link '}):
            mp3_list.append('http://www.youtube.com'+str(song_link.get('href')))

        return mp3_list
    def download(self, url, dir = None):
        self.url = url
        self.dir = dir
        api_url = 'http://www.youtubeinmp3.com/fetch/?video='
        song_name_list = []
        source_html = requests.get(self.url).text
        soup = BeautifulSoup(source_html, 'html.parser')
        for song_name in soup.find_all('a',{'class':'pl-video-title-link yt-uix-tile-link yt-uix-sessionlink  spf-link '}):
            song_name_list.append(unicode(song_name.string).strip())
        if self.dir == None:
            for x in range(0, len(song_name_list)):
                mp3file = urllib2.urlopen(api_url+self.get_mp3_list()[x])
                with open(song_name_list[x]+'.mp3', 'wb') as output:
                    output.write(mp3file.read())
        if self.dir != None:
            for x in range(0, len(song_name_list)):
                mp3file = urllib2.urlopen(api_url+self.get_mp3_list()[x])
                with open(self.dir+song_name_list[x]+'.mp3', 'wb') as output:
                    output.write(mp3file.read())

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('service',help = 'Select if you want to download either one youtube video or a youtube playlist',type = str, choices =['youtube','youtube_playlist'])
    parser.add_argument('url',help = 'insert the url of the video or playlist you would like to download', type = str)
    parser.add_argument('--directory', help ='specify the download location for the file/files', type = str)
    args = parser.parse_args()
    downloader = None
    if args.service == 'youtube' and args.directory == None:
        downloader = YoutubeDownloader()
        downloader.download(args.url)
    elif args.service == 'youtube_playlist' and args.directory == None:
        downloader = YoutubePlaylistDownloader()
        downloader.download(args.url)
    elif args.service == 'youtube' and args.directory != None:
        downloader = YoutubeDownloader()
        downloader.download(args.url, args.directory)
    elif args.service == 'youtube_playlist' and args.directory != None:
        downloader = YoutubePlaylistDownloader()
        downloader.download(args.url, arg.directory)





#downloader = YoutubePlaylistDownloader()

#file = downloader.download('https://www.youtube.com/playlist?list=PLlE8_K_sXIXtRYhDHwgT4kvKwmJhbibbd')




