import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    def __init__(self):
        self.base_url = r'https://petfriends1.herokuapp.com/'

    def _get_status_result(self, response):
        """
        Получает код ответа (status_code) и тело ответа из response
        :param response: Ответ, возвращаемый функциями модуля requests (get, post, delete, put
        :return: кортеж (код ответа, тело ответа)
        """
        status = response.status_code
        try:
            result = response.json()
        except:
            result = response.text
        return status, result

    def get_api_key(self, email: str, password: str) -> tuple:
        """
        Возвращает API key по e-mail и паролю
        """
        headers = {
            'email': email,
            'password': password,
        }
        response = requests.get(self.base_url + 'api/key', headers=headers)
        return self._get_status_result(response)

    def get_list_of_pets(self, auth_key: dict, filter: str = '') -> tuple:
        """
        Возвращает список питомцев
        """
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        response = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        return self._get_status_result(response)

    def add_new_pet(self, auth_key: dict, pet_data: dict) -> tuple:
        """
        Добавлет нового питомца
        """
        photo_file = open(pet_data['pet_photo'], 'rb')
        data = MultipartEncoder(
            fields={
                'name': pet_data['name'],
                'animal_type': pet_data['animal_type'],
                'age': pet_data['age'],
                'pet_photo': (pet_data['pet_photo'], photo_file, 'image/jpeg')
                if pet_data['pet_photo'] != '' else ''
            })
        headers = {
            'auth_key': auth_key['key'],
            'Content-Type': data.content_type
        }
        response = requests.post(self.base_url + 'api/pets', headers=headers, data=data)

        if not photo_file.closed:
            photo_file.close()

        return self._get_status_result(response)

    def delete_pet(self, auth_key: dict, pet_id: str) -> tuple:
        """
        Удаляет питомца
        """
        headers = {
            'auth_key': auth_key['key'],
        }
        response = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        return self._get_status_result(response)

    def update_pet(self, auth_key: dict, pet_id: str, pet_data: dict) -> tuple:
        """
        Обновляет данные питомца
        """
        headers = {
            'auth_key': auth_key['key'],
        }
        response = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=pet_data)
        return self._get_status_result(response)
