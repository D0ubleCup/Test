import requests


class VKapi:
    __url = 'https://api.vk.com/method/wall.post'
    __headers = {'Authorization': 'Bearer vk1.a.7qQauj0yBtN9DIZMe6Gx6fkfIAlub0ZGGXcVR7uF3Id1xjfDuyIQpyZzMw06GX3rZeROe2X_TqyR1WtxZ9t8spUYsXhGhWiFBpiQe1sF9AG_C26i3letT3Z_CdvWg9W0E2fSvSMEyfEbCVC0Slu55RCIzW2bzgK5_lc0Rd8HnQTOoHV65M0Rhy6kJ5nVngTxn_xywD70d1EdPyL_iXqFDw'}
    __params = {}

    def __init__(self, data: dict) -> None:
        self.network = data['network']
        self.post_text = data['post_text']
        self.photo = data['photo']
    
    def add_settings(self, data: dict) -> None:
        """Добавление прочих функции"""
        key = list(data.keys())[0]
        self.__params[key] = data[key]
    

    def work_api(self):
        responce = requests.get(url=self.__url, headers=self.__headers, params=self.__params).text
        return self.errors(responce)
    
    def errors(self, responce):
        pass