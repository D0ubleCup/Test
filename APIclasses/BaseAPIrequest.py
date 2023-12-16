import requests
import os

from dotenv import load_dotenv
load_dotenv()



VK_TOKEN = os.getenv('VK_TOKEN')

class VKapi:

    __url = 'https://api.vk.com/method/wall.post'
    __headers = {'Authorization': f'Bearer {VK_TOKEN}'}
    __params = {'message':None, 'attachments':None, 'friends_only': 0, 'close_comments': 0, 'v':'5.199'}
    __photo_path = None   
    error_codes = {
        #общие ошибки
        1 : 'Произошла неизвестная ошибка. Попробуйте повторить запрос позже',
        2 : 'Приложение выключено, включите его в настройках',
        10 :'Произошла внутренняя ошибка сервера. Попробуйте повторить запрос позже',
        11 : 'В тестовом режиме приложение должно быть выключено или пользователь должен быть залогинен',
        18 : 'Страница удалена или заблокирована',
        300 : 'Альбом на странице переполнен, фотографий должно быть меньше 500',
        #ошибки wall.post
        214 : 'Доступ к добавлению записи запрещен',
        219 : 'Недавно был добавлен рекламный пост',
        222 : 'Гиперссылки запрещены',
        #ошибки saveWallPhoto
        22 : 'Ошибка загрузки фотографии',
        114 : 'Неверный идентификатор альбома',
        118 : 'Ошибка со стороны сервера (сервер не действителен)',
        121 : 'Ошибка загрузки фотографии(неверный хэш)'
    } 
    
    def __init__(self, data: dict) -> None:
        self.__params['message'] = data['post_text']
        self.__photo_path = data['photo']


    def add_settings(self, data: dict) -> None:
        """Добавление прочих функции
        Принимает словарь {параметр : значение}"""
        key = list(data.keys())[0]
        self.__params[key] = data[key]

    def get_data(self) -> dict:
        """Геттер, возвращает параметры записи"""
        params = self.__params
        params['attachments'] = self.__photo_path #вставляем название фотографии
        return params
    
    def ready_post(self) -> bool:
        """Готовность записи к постингу"""
        if self.__params['message'] is not None and self.__photo_path is not None: #определяет наличие основных параметров для постинга (текст и фото)
            return True
        return False

    
    def work_api(self) -> str: 
        """Публикация записи"""
        photo_link = self.__photo_link(self.__photo_path) #преобразуем фотографию в ссылку для запроса

        if  photo_link[0]: 
            return f'Ошибка во время загрузки фотографии - {photo_link[1]}'
        
        self.__params['attachments'] = photo_link[1] #записываем в параметры
        response = requests.get(url=self.__url, headers=self.__headers, params=self.__params)
        
        answer = self.__errors(response) #обрабатываем запрос
        if answer[0]:  f'Ошибка при публикации {answer[1]}' 
        return answer[1]
    
    @classmethod 
    def __errors(self, response) -> list:
        """Обработка запроса, вывод ошибок
        Возвращает список [bool, 'info']
        bool -> True имеется ошибка
        bool -> False Если ошибок нет
        """
        if response.status_code not in (200, 201):
            return [True , 'Серверная ошибка']
        if 'error' in response.text:
            key_error = response.json()['error']['error_code']
            return [True, self.error_codes[key_error]] 
        return [False, 'Запись успешно выложена']

    
    @classmethod 
    def __photo_link(self, path_photo: str) -> str: 
        """Возвращает список [bool, 'параметр attachments для фотографии']
        bool -> True имеется ошибка
        bool -> False Если ошибок нет
        """

        """https://dev.vk.com/ru/api/upload/wall-photo#Публикация%20фотографии"""
        headers = self.__headers

        url = 'https://api.vk.com/method/photos.getWallUploadServer'
        params = {'v':'5.131'}
        response = requests.get(url=url, headers=headers,params=params)

        err = self.__errors(response) 
        if err[0]: return err    #проверяет на наличие ошибок в запросе

        url1 = response.json()['response']['upload_url']
        path = os.path.join(os.getcwd(), 'content',f'{path_photo}.jpg')
        files = {'photo': open(path, 'rb')}
        response = requests.post(url=url1,headers=headers,files=files)

        err = self.__errors(response)
        if err[0]: return err

  
        url2 = 'https://api.vk.com/method/photos.saveWallPhoto'
        params = response.json()
        params['v'] = '5.131'
        response = requests.get(url=url2, headers=headers, params=params)

        err = self.__errors(response)
        if err[0]: return err

        owner_id = response.json()['response'][0]['owner_id']
        ids = response.json()['response'][0]['id']
        attachments = f'photo{owner_id}_{ids}'  #строим нужную нам ссылку
        return [False, attachments]

    def __del__(self) -> None:
        file_path = f'content/{self.__photo_path}.jpg'
        self.__params = {'message':None, 'attachments':None, 'friends_only': 0, 'close_comments': 0, 'v':'5.199'}
        self.__photo_path = None
        if file_path:
            if os.path.isfile(path=file_path):
                os.remove(path=file_path)
