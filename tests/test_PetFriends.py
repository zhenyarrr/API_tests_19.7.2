from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_age
import os

pf = PetFriends()

def test_get_api_key_for_invalid_user(email=invalid_email, password=valid_password):
    """Проверяем, что запрос ключа от несуществубщего пользователя не возвращает статус 200"""
    #Отправляем запрос и сохраняем полученный ответ с кодом статуса в status
    status = pf.get_api_key(email, password)
    # Проверяем:
    assert status != 200
    print(status)

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем, что запрос API ключа возвращает статус 200
    и в результате содержится слово key"""

    #Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    #Сверяем фактический результат с ожидаемым
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """Запрос всех питомцев возвращаем не пустой список.
    Получаем API ключ и сохраняем в переменную auth_key.
    Далее используя этот ключ запрашиваем список всех питомцев и проверяем,
    что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_get_all_pets_with_invalid_key(filter=''):
    """Запрос всех питомцев возвращаем не пустой список.
    Получаем API ключ и сохраняем в переменную auth_key.
    Далее используя этот ключ запрашиваем список всех питомцев и проверяем,
    что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(invalid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status != 200

def test_add_new_pet_with_valid_data(name='Charlik', animal_type='dog', age='4', pet_photo='images/Пинчер.jpg'):
    """Проверяем, что можно добавить питомца с корректными данными"""

    #Получаем полный пусть изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    #Запрашиваем ключ API и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    #Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    #Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_invalid_age(name='Kesha', animal_type='parrot', age=invalid_age, pet_photo='images/Попугайчик.jpg'):
    """Проверяем, что возраст питомца нельзя обозначить символами"""

    #Получаем полный пусть изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    #Запрашиваем ключ API и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    #Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    #Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result[age] is int


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    #Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    #Проверяем, что если список своих питомцев пустой, то добавление нового
    #и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Сharlik", "пес", '4', "images/Пинчер.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")


    #Берем id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    #Еще раз запрашиваем список сових питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    #Проверяем, что статус ответа равен 200 и в списке питомцев нет id удаленного питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Бим', animal_type='собака', age='6'):
    """Проверяем возможность обновления информации о питомце"""

    #Получаем ключ auth_key и список сових питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то обновляем имя, тип и возраст питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name

    else:
        # Если список питомцев пуст, то выводим сообщение с текстом об отсутствии питомцев в своем списке
        raise Exception("There is no my pets")

def test_add_new_pet_no_photo_with_valid_data(name='Cat_no_photo', animal_type='cat', age='1'):
    """Проверяем что можно быстро добавить питомца без фото с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_pet_no_photo(auth_key, name, animal_type, age)

    # Сверяем фактический результат с ожидаемым
    assert status == 200
    assert result['name'] == name
    assert result['pet_photo'] is ''


def test_successful_update_self_pet_photo(pet_photo='images/Пинчер.jpg'):
    """Проверяем возможность добавления фото к питомцу"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то обновляем фото питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['pet_photo'] is not ''  # (сообщение об ошибке)

    else:
        # Если список питомцев пуст, то выводим сообщение с текстом об отсутствии питомцев в своем списке
        raise Exception("There is no my pets")
