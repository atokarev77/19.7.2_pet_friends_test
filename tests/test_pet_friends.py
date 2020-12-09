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


    def test_delete_pet_with_valid_id(self):
        auth_key = self._get_auth_key()

        # Get list of my pets
        status, result = pf.get_list_of_pets(auth_key, 'my_pets')
        if len(result['pets']) == 0:
            status, result = pf.add_new_pet(auth_key, self.my_pet)
            deleted_pet_id = result['id']
        else:
            deleted_pet_id = result['pets'][0]['id']

        status, result = pf.delete_pet(auth_key, deleted_pet_id)
        assert status == 200

        # Check that the deleted pet is not in the pet's list
        status, result = pf.get_list_of_pets(auth_key)
        pet_deleted = True
        for pet in result['pets']:
            if pet['id'] == deleted_pet_id:
                pet_deleted = False
                break
        assert pet_deleted

    # ============================================

    def test_get_api_key_for_invalid_password(self):
        """
        Тестирует получение API key по валидному e-mail, но с неверным паролем
        """

        status, result = pf.get_api_key(email=settings.valid_email, password=settings.invalid_password)
        assert status == 403
        assert "user wasn't found" in result

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

    def test_add_new_pet_with_HTML(self):
        """
        Тестирует добавление питомца с HTML кодом в качестве name и animal_type
        Идею подсказал сокурсник @Alexandr Plakhotnikov в Slack
        """

        auth_key = self._get_auth_key()
        name_HTML = """
                    <html>
                    <head>
                    <title>Пример 1</title>
                    </head>
                    <body>
                    <H1>Привет!</H1>
                    <P> Это простейший пример HTML-документа. </P>
                    </body>
                    </html>
                    """
        animal_type_HTML = """
                        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
                        <html>
                         <head>
                          <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                          <title>Пример веб-страницы</title>
                         </head>
                         <body>
                          <h1>Заголовок</h1>
                          <!-- Комментарий -->
                          <p>Первый абзац.</p>
                          <p>Второй абзац.</p>
                         </body>
                        </html>
                        """
        pet_data = {
            'name': name_HTML,
            'animal_type': animal_type_HTML,
            'age': self.my_pet['age'],
            'pet_photo': self.my_pet['pet_photo']
        }

        status, result = pf.add_new_pet(auth_key, pet_data=pet_data)
        assert status == 200
        if type(result) == dict:
            assert result['name'] == pet_data['name']\
                 and result['animal_type'] == pet_data['animal_type'] \
                 and result['age'] == pet_data['age']

    def test_get_all_pets_with_invalid_filter(self):
        """
        Тестирует получение списка питомцев с валидным API key, но фильтром из случайных символов
        """

        auth_key = self._get_auth_key()
        status, result = pf.get_list_of_pets(auth_key, ';lqw;nf;qw;ws;')
        assert status == 200
        assert len(result['pets']) == 0





