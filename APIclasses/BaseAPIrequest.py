import requests
import os


class VKapi:

    __url = 'https://api.vk.com/method/wall.post'
    __headers = {'Authorization': 'Bearer vk1.a.7qQauj0yBtN9DIZMe6Gx6fkfIAlub0ZGGXcVR7uF3Id1xjfDuyIQpyZzMw06GX3rZeROe2X_TqyR1WtxZ9t8spUYsXhGhWiFBpiQe1sF9AG_C26i3letT3Z_CdvWg9W0E2fSvSMEyfEbCVC0Slu55RCIzW2bzgK5_lc0Rd8HnQTOoHV65M0Rhy6kJ5nVngTxn_xywD70d1EdPyL_iXqFDw'}
    __params = {'post_text':None, 'photo':None, 'friends_only': False, 'close_comments': False, 'v':'5.199'}
    
    def __init__(self, data: dict) -> None:
        self.__params['post_text'] = data['post_text']
        self.__params['photo'] = data['photo']

    def add_settings(self, data: dict) -> None:
        """Добавление прочих функции"""
        key = list(data.keys())[0]
        self.__params[key] = data[key]

    def get_data(self) -> dict:
        return self.__params

    
    def work_api(self):
        """Публикация записи"""
        self.__params['photo'] = self.__photo_link(self.__params['photo'])
        response = requests.get(url=self.__url, headers=self.__headers, params=self.__params)
        print(response.text)
        return self.__errors(response)
    
    @classmethod 
    def __photo_link(self, path_photo: str) -> str: #content/name.jpg
        """Возвращает параметр attachments"""
        headers = self.__headers

        url = 'https://api.vk.com/method/photos.getWallUploadServer'
        params = {'v':'5.131'}
        response = requests.get(url=url, headers=headers,params=params).json()

        url1 = response['response']['upload_url']
        print(path_photo)
        path = os.path.join(os.getcwd(), 'content',f'{path_photo}.jpg')
        print(path)
        files = {'photo': open(path, 'rb')}
        response = requests.post(url=url1,headers=headers,files=files).json()

  
        url2 = 'https://api.vk.com/method/photos.saveWallPhoto'
        params = response
        params['v'] = '5.131'
        response = requests.get(url=url2, headers=headers, params=params).json()

        owner_id = response['response'][0]['owner_id']
        ids = response['response'][0]['id']
        attachments = f'photo{owner_id}_{ids}'
        return attachments
    
    def __errors(self, response):
        """Обработка запроса"""
        if response.status_code in (200, 201):
            return 'True'
        return response.json()['response']['error_msg']

    def __del__(self):
        file_path = self.__params['photo']
        self.__params = {'post_text':None, 'photo':None}
        if file_path:
            if os.path.isfile(path=file_path):
                os.remove(path=file_path) 
