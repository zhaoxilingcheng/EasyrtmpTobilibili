import os
from ffmpy3 import FFmpeg
import configparser
import csv

config = configparser.ConfigParser()

config.read("conf", encoding="utf-8")

videotxtpath=config.get("videodir", "video_list")
videodir = config.get("videodir", "dir")
if os.path.exists(videotxtpath):
    live_address = config.get("rtmp", "live_address")
    live_code = config.get("rtmp", "live_code")
    rtmp_url = live_address+live_code

    print(rtmp_url)
    videolist = {}
    with open(videotxtpath, "r") as videotxt:
        reader = csv.reader(videotxt)
        for line in reader:
            videolist[int(line[1])] = videodir+'/'+line[0]
    videolistsize = len(videolist)
    while(1):
        for i in range(1, videolistsize+1):
            ff = FFmpeg(
                inputs={videolist[i]:'-re '},
                outputs={rtmp_url:'-vcodec copy -acodec aac -b:a 192k -f flv'}
            )
            print(ff.cmd)
            ff.run()
else:
    print("no videotxtpath in dir plase run the listvideo.py first.")