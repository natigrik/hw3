import pytest
import requests
from jsonschema import validate
import json


# получение списков пород (с видами) и основных пород для использования в запросах
resp = requests.get("https://dog.ceo/api/breeds/list/all")

# TODO проверить, можно ли тут обойтись без записи в файл, работая напрямую с ответом
# with open("all_breeds.json", "w") as r:
#     json.dump(resp.json(), r)
#
# with open('all_breeds.json', "r") as u:
#     breeds_list = json.loads(u.read())
#     for key, value in breeds_list.items():
#         if key == 'message':
#             breeds = value


breeds_list = resp.json()
breeds = []
for key, value in breeds_list.items():
    if key == 'message':
        breeds = value
breeds_all = []
breeds_main = []

for key, value in breeds.items():
    breeds_main.append(key)
    if not value:
        breeds_all.append(key)
    else:
        for i in value:
            breeds_all.append(i + " " + key)


# тесты на валидность формата ответа
def test_list_all_schema(base_url):
    res = requests.get(base_url + "/api/breeds/list/all")

    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "object"},
            "status": {"type": "string"},
        },
        "required": ["message", "status"]
    }

    validate(instance=res.json(), schema=schema)


def test_random_image_schema(base_url):
    res = requests.get(base_url + "/api/breeds/image/random")

    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "string"},
            "status": {"type": "string"},
        },
        "required": ["message", "status"]
    }

    validate(instance=res.json(), schema=schema)


@pytest.mark.parametrize('breed_name', breeds_main)
# @pytest.mark.parametrize('breed_name', ['terrier', 'test'])
@pytest.mark.parametrize('list_type', ['/images', '/list'])
def test_breed_list_schema(base_url, list_type, breed_name):
    res = requests.get(base_url + "/api/breed/" + breed_name + list_type)

    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "array"},
            "status": {"type": "string"},
        },
        "required": ["message", "status"]
    }

    validate(instance=res.json(), schema=schema)


# @pytest.mark.parametrize('breed', breeds_all)
@pytest.mark.parametrize('breed', ['toy terrier', 'test'])
def test_breed_list(base_url, breed):
    res = requests.get(base_url + "/api/breed/" + breed + "/images/random")

    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "string"},
            "status": {"type": "string"},
            "code": {"type": "number"}
        },
        "required": ["message", "status"]
    }

    validate(instance=res.json(), schema=schema)

