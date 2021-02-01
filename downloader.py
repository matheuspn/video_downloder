import youtube_dl
import json


class MyLogger(object):
    def debug(self, msg):
        print("Debug: ", msg)

    def warning(self, msg):
        print("Warning: ", msg)

    def error(self, msg):
        print("Error: ",msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

with open("ydl_opts.json", "r") as f:
    ydl_opts = json.load(f)

def baixar(url, opt):

    ydl_opts[opt]['logger'] = MyLogger()
    ydl_opts[opt]['progress_hooks'] = [my_hook]

    with youtube_dl.YoutubeDL(ydl_opts[opt]) as ydl:
        ydl.download([url])

    return True

def get_info(url):
    ydl_opts = {}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(url, download=False) 

    try:
        meta['thumbnail'] 
    except:
        meta['thumbnail'] = 'std_img.jpg'
        return [meta['title'], meta['thumbnail']]
    finally:
        return [meta['title'], meta['thumbnail']]
