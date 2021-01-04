import youtube_dl


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


ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    },
        {'key': 'EmbedThumbnail'},
        {'key': 'FFmpegMetadata'},
        ],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
    'writethumbnail': True,
}

def baixar(url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return True

def get_info(url):
    ydl_opts = {}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(url, download=False) 

    try:
        meta['thumbnail'] 
    except:
        meta['thumbnail'] = 'imagem_padrao.jpg'
        return [meta['title'], meta['thumbnail']]
    finally:
        return [meta['title'], meta['thumbnail']]
