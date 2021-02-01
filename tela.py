from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularElevationBehavior

import asyncio
from downloader import baixar, get_info


class Home(MDBoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = self.create_menu(
                "test", self.ids.toolbar.ids.menu_button,
            )

    # menu
    def create_menu(self, text, instance):
        menu_items = [{"icon": "git", "text": text} for i in range(5)]
        menu = MDDropdownMenu(caller=instance, items=menu_items, width_mult=5)
        menu.bind(on_release=self.menu_callback)
        return menu

    def menu_callback(self, instance_menu, instance_menu_item):
        instance_menu.dismiss()


    def options(self):
        print("Cog test")

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



class CustomToolbar(ThemableBehavior, RectangularElevationBehavior, MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = self.theme_cls.primary_dark

class Tela(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Home()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Tela().async_run(async_lib='asyncio'))
    loop.close()

# https://www.youtube.com/watch?v=sJSR5-VOlRc