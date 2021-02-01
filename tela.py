import asyncio

from kivy.uix.screenmanager import ScreenManager

from downloader import baixar, get_info
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen


class Configs(MDScreen):
    
    def teste(self, checkbox, value):
        if value:
            print(f"{checkbox}ativado")
        else: print(f"{checkbox}desativado")

class Home(MDScreen):

    def download(self):
        self.ids.status.text = "baixando ..."
        url = self.ids.url_text.text
        asyncio.create_task(Home.info(self, url))
        asyncio.create_task(Home.baixa(self, url))

    # chama a função download 
    async def baixa(self, url):
        acabou = await asyncio.to_thread(baixar, url= url, opt= 0)
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

class ScreenMngr(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = self.create_menu("test", self.ids.home.ids.toolbar.ids.menu_button,)

    # menu
    def create_menu(self, text, instance):
        menu_items = [
            {"text": "Configurações"},
            {"text": "Tema claro"}
        ]
        menu = MDDropdownMenu(caller=instance, items=menu_items, width_mult=3)
        menu.bind(on_release=self.menu_callback)
        return menu

    def menu_callback(self, instance_menu, instance_menu_item):
        app = MDApp.get_running_app()

        if instance_menu_item.text == "Configurações":
            self.current = "config"
            instance_menu.dismiss()
        # trocando os temas entre claro e escuro
        elif instance_menu_item.text.startswith("Tema"):
            tema = instance_menu_item.text
            if tema == "Tema escuro":
                app.theme_cls.theme_style = "Dark"
                instance_menu_item.text = "Tema claro"
            elif tema == "Tema claro":
                app.theme_cls.theme_style = "Light"
                instance_menu_item.text = "Tema escuro"
        else:
            instance_menu.dismiss()
        #print(instance_menu, instance_menu_item)

class Tela(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return ScreenMngr()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Tela().async_run(async_lib='asyncio'))
    loop.close()

# https://www.youtube.com/watch?v=sJSR5-VOlRc