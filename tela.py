from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

import asyncio
from downloader import baixar, get_info


class Home(MDBoxLayout):
    
    def download(self):
        self.ids.status.text = "baixando ..."
        url = self.ids.url_text.text
        asyncio.create_task(Home.info(self,url))
        asyncio.create_task(Home.baixa(self, url))


    # chama a função download 
    async def baixa(self, url):
        #acabou = await asyncio.to_thread(baixar, url= url)
        self.ids.status.text = "concluído"

    # pega as informações do vídeo baixado
    async def info(self, url):
        meta = await asyncio.to_thread(get_info, url= url)
        # adiciona a thumb na tela com o título
        self.ids.box.add_widget(Video(video_text= meta[0], video_image= meta[1]))

class Video(MDBoxLayout):
    def __init__(self,video_text='',video_image= '',**kwargs):
        super().__init__(**kwargs)
        self.ids.video_text.text = video_text
        self.ids.video_image.source = video_image

class Tela(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Home()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Tela().async_run(async_lib='asyncio'))
    loop.close()

# https://www.youtube.com/watch?v=sJSR5-VOlRc