import json
import requests
### Returns pet inventories by status ###
res11 = requests.get(f'https://petfriends.skillfactory.ru/api/key', headers={'accept':'application/json', 'email':'zhenya_rakushina@mail.ru', 'password': 'Password1', 'Content-Type': 'application/xml'})
print("API Key:", res11.status_code)
print(res11.text)


data = {'name': "", 'animal_type': '', 'age': ''}
headers = {'auth_key': '4be94c5086ddb72a7dd417ab0afc09994ec25fc9df325ccb6367aa12'}

res = requests.post(f'https://petfriends.skillfactory.ru/api/create_pet_simple', headers=headers, data=data)
print("Add without a photo:", res.status_code)
print(res.text)