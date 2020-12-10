"""
Модуль содержит только 10 тестов для задания 19.7.2
"""

import api
import settings
import os


pf = api.PetFriends()


class TestPetFriends:

    def setup(self):
        pet_photo = os.path.join('..', 'images', 'dog.jpg')
        self.my_pet = {
            'name': 'Billy',
            'animal_type': 'Dog',
            'age': '2',
            'pet_photo': os.path.join(os.path.dirname(__file__), pet_photo)
        }

    def _get_auth_key(self, email: str=settings.valid_email, password: str=settings.valid_password) -> dict:
        """
        Получает API key по e-mail и password
        :return: Словарь с ключом key и значением API key
        """

        status, result = pf.get_api_key(email, password)
        return result

    def test_get_api_key_for_invalid_password(self):
        """
        Тестирует получение API key по валидному e-mail, но с неверным паролем
        """

        status, result = pf.get_api_key(email=settings.valid_email, password=settings.invalid_password)
        assert status == 403
        assert "user wasn't found" in result

    def test_get_api_key_for_invalid_email(self):
        """
        Тестирует получение API key по невалидному по формату e-mail
        """

        status, result = pf.get_api_key(email=settings.invalid_email, password=settings.valid_password)
        assert status == 403
        assert "user wasn't found" in result

    def test_get_api_key_for_huge_email_and_password(self):
        """
        Тестирует получение API key по очень большим и невалидным e-mail и паролю
        """

        status, result = pf.get_api_key(email=settings.huge_text_without_returns,
                                        password=settings.huge_text_without_returns)
        assert status == 400

    def test_update_pet_with_invalid_id(self):
        """
        Тестирует обновление данных питомца по неверному id питомца
        """

        auth_key = self._get_auth_key()
        updated_pet_id = "wrong pet ID"
        pet_data = {
            'name': 'Josey',
            'animal_type': 'cat',
            'age': '100'
        }
        status, result = pf.update_pet(auth_key, updated_pet_id, pet_data)
        assert status == 400
        assert "id wasn't found" in result

    def test_add_new_pet_with_html(self):
        """
        Тестирует добавление питомца с HTML кодом в качестве name, animal_type и age
        Идею подсказал сокурсник @Alexandr Plakhotnikov в Slack
        """

        auth_key = self._get_auth_key()
        pet_data = {
            'name': settings.name_HTML,
            'animal_type': settings.animal_type_HTML,
            'age': settings.animal_type_HTML,
            'pet_photo': self.my_pet['pet_photo']
        }

        status, result = pf.add_new_pet(auth_key, pet_data=pet_data)
        assert status == 200
        if type(result) == dict:
            assert result['name'] == pet_data['name']\
                 and result['animal_type'] == pet_data['animal_type'] \
                 and result['age'] == pet_data['age']

    def test_add_new_pet_with_empty_data(self):
        """
        Тестирует добавление питомца с пустыми значениями во всех полях
        """

        auth_key = self._get_auth_key()
        pet_data = {
            'name': '',
            'animal_type': '',
            'age': '',
            'pet_photo': ''
        }

        status, result = pf.add_new_pet(auth_key, pet_data=pet_data)
        assert status == 400

    def test_add_new_pet_with_huge_text(self):
        """
        Тестирует добавление питомца с большим текстом в качестве name, animal_type и age
        """

        auth_key = self._get_auth_key()
        pet_data = {
            'name': settings.huge_text,
            'animal_type': settings.huge_text,
            'age': settings.huge_text,
            'pet_photo': self.my_pet['pet_photo']
        }

        status, result = pf.add_new_pet(auth_key, pet_data=pet_data)
        assert status == 200
        if type(result) == dict:
            assert result['name'] == pet_data['name']\
                 and result['animal_type'] == pet_data['animal_type'] \
                 and result['age'] == pet_data['age']
        """ 
        Питомец добавляетс, но при отображении в списке всех питомцев 
        строки не обрезаются, и карточка питомца занимает очень много места по вертикали
        """

    def test_get_all_pets_with_invalid_filter(self):
        """
        Тестирует получение списка питомцев с валидным API key, но фильтром из случайных символов
        """

        auth_key = self._get_auth_key()
        status, result = pf.get_list_of_pets(auth_key, ';lqw;nf;qw;ws;')

        # В норме систем должна при неверном фильтре просто вернуть пустой список питомцев
        # а не ошибку сервера 500
        assert status == 200
        assert len(result['pets']) == 0

    def test_get_all_pets_with_invalid_key(self):
        """
        Тестирует получение списка питомцев с невалидным API key
        1) пустым API key
        2) содержащим спецсимволы и символы кириллицы
        """

        auth_key = {'key': ''}
        status, result = pf.get_list_of_pets(auth_key)
        assert status == 403
        assert "provide 'auth_key'" in result

        auth_key = {'key': r'Wrong API key */*!";"%:№?*(())88966 Неверный АПИ ключ'.encode(encoding='utf-8')}
        status, result = pf.get_list_of_pets(auth_key)
        assert status == 403
        assert "provide 'auth_key'" in result

    def test_delete_pet_with_invalid_id(self):
        """
        Тестирует удаление питомца по невалидному id
        """

        auth_key = self._get_auth_key()
        deleted_pet_id = "wrong pet ID Неверный ID"
        status, result = pf.delete_pet(auth_key, deleted_pet_id)

        # В норме система должна сообщить, что питомец с таким id не найден
        assert status == 400
        assert "id wasn't found" in result



