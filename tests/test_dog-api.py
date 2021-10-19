import pytest
import requests
from jsonschema import validate
import json


# массивы со списками пород для параметризации
breeds_all = ['affenpinscher', 'african', 'airedale', 'akita', 'appenzeller', 'shepherd australian', 'basenji', 'beagle', 'bluetick', 'borzoi', 'bouvier', 'boxer', 'brabancon', 'briard', 'norwegian buhund', 'boston bulldog', 'english bulldog', 'french bulldog', 'staffordshire bullterrier', 'australian cattledog', 'chihuahua', 'chow', 'clumber', 'cockapoo', 'border collie', 'coonhound', 'cardigan corgi', 'cotondetulear', 'dachshund', 'dalmatian', 'great dane', 'scottish deerhound', 'dhole', 'dingo', 'doberman', 'norwegian elkhound', 'entlebucher', 'eskimo', 'lapphund finnish', 'bichon frise', 'germanshepherd', 'italian greyhound', 'groenendael', 'havanese', 'afghan hound', 'basset hound', 'blood hound', 'english hound', 'ibizan hound', 'plott hound', 'walker hound', 'husky', 'keeshond', 'kelpie', 'komondor', 'kuvasz', 'labradoodle', 'labrador', 'leonberg', 'lhasa', 'malamute', 'malinois', 'maltese', 'bull mastiff', 'english mastiff', 'tibetan mastiff', 'mexicanhairless', 'mix', 'bernese mountain', 'swiss mountain', 'newfoundland', 'otterhound', 'caucasian ovcharka', 'papillon', 'pekinese', 'pembroke', 'miniature pinscher', 'pitbull', 'german pointer', 'germanlonghair pointer', 'pomeranian', 'miniature poodle', 'standard poodle', 'toy poodle', 'pug', 'puggle', 'pyrenees', 'redbone', 'chesapeake retriever', 'curly retriever', 'flatcoated retriever', 'golden retriever', 'rhodesian ridgeback', 'rottweiler', 'saluki', 'samoyed', 'schipperke', 'giant schnauzer', 'miniature schnauzer', 'english setter', 'gordon setter', 'irish setter', 'english sheepdog', 'shetland sheepdog', 'shiba', 'shihtzu', 'blenheim spaniel', 'brittany spaniel', 'cocker spaniel', 'irish spaniel', 'japanese spaniel', 'sussex spaniel', 'welsh spaniel', 'english springer', 'stbernard', 'american terrier', 'australian terrier', 'bedlington terrier', 'border terrier', 'cairn terrier', 'dandie terrier', 'fox terrier', 'irish terrier', 'kerryblue terrier', 'lakeland terrier', 'norfolk terrier', 'norwich terrier', 'patterdale terrier', 'russell terrier', 'scottish terrier', 'sealyham terrier', 'silky terrier', 'tibetan terrier', 'toy terrier', 'westhighland terrier', 'wheaten terrier', 'yorkshire terrier', 'vizsla', 'spanish waterdog', 'weimaraner', 'whippet', 'irish wolfhound']
breeds_main = ['affenpinscher', 'african', 'airedale', 'akita', 'appenzeller', 'australian', 'basenji', 'beagle', 'bluetick', 'borzoi', 'bouvier', 'boxer', 'brabancon', 'briard', 'buhund', 'bulldog', 'bullterrier', 'cattledog', 'chihuahua', 'chow', 'clumber', 'cockapoo', 'collie', 'coonhound', 'corgi', 'cotondetulear', 'dachshund', 'dalmatian', 'dane', 'deerhound', 'dhole', 'dingo', 'doberman', 'elkhound', 'entlebucher', 'eskimo', 'finnish', 'frise', 'germanshepherd', 'greyhound', 'groenendael', 'havanese', 'hound', 'husky', 'keeshond', 'kelpie', 'komondor', 'kuvasz', 'labradoodle', 'labrador', 'leonberg', 'lhasa', 'malamute', 'malinois', 'maltese', 'mastiff', 'mexicanhairless', 'mix', 'mountain', 'newfoundland', 'otterhound', 'ovcharka', 'papillon', 'pekinese', 'pembroke', 'pinscher', 'pitbull', 'pointer', 'pomeranian', 'poodle', 'pug', 'puggle', 'pyrenees', 'redbone', 'retriever', 'ridgeback', 'rottweiler', 'saluki', 'samoyed', 'schipperke', 'schnauzer', 'setter', 'sheepdog', 'shiba', 'shihtzu', 'spaniel', 'springer', 'stbernard', 'terrier', 'vizsla', 'waterdog', 'weimaraner', 'whippet', 'wolfhound']


# получение полного списка пород
def test_list_all_schema(base_url):
    res = requests.get(base_url + "/api/breeds/list/all")
    assert res.status_code == 200

    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "object"},
            "status": {"type": "string"},
        },
        "required": ["message", "status"]
    }

    validate(instance=res.json(), schema=schema)


# получение случайной картинки любой породы
def test_random_image_schema(base_url):
    res = requests.get(base_url + "/api/breeds/image/random")
    assert res.status_code == 200

    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "string"},
            "status": {"type": "string"},
        },
        "required": ["message", "status"]
    }

    validate(instance=res.json(), schema=schema)


# получение нескольких случайных картинок любых пород
def test_some_random_image_schema(base_url):
    res = requests.get(base_url + "/api/breeds/image/random/1")
    assert res.status_code == 200

    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "array"},
            "status": {"type": "string"},
        },
        "required": ["message", "status"]
    }

    validate(instance=res.json(), schema=schema)


@pytest.mark.parametrize('count_images', ['1', '49', '50', '51', '100'])
def test_some_random_image_count(base_url, count_images):
    res = requests.get(base_url + "/api/breeds/image/random/" + count_images)
    assert res.status_code == 200

    images_list = res.json()
    images = []
    for key1, value1 in images_list.items():
        if key1 == 'message':
            images = value1

    count_images1 = int(count_images)
    if count_images1 <= 50:
        assert len(images) == count_images1
    else:
        assert len(images) == 50


# получение списка картинок и списка подвидов по основной породе
# TODO найти, как сделать случайный выбор параметра из списка, чтобы не прогонять все породы
# @pytest.mark.parametrize('breed_name', breeds_main)
@pytest.mark.parametrize('breed_name', ['terrier'])
@pytest.mark.parametrize('list_type', ['/images', '/list'])
def test_breed_list_schema(base_url, list_type, breed_name):
    res = requests.get(base_url + "/api/breed/" + breed_name + list_type)
    assert res.status_code == 200

    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "array"},
            "status": {"type": "string"},
        },
        "required": ["message", "status"]
    }

    validate(instance=res.json(), schema=schema)


# получение случайной картинки по основной породе
# TODO найти, как сделать случайный выбор параметра из списка, чтобы не прогонять все породы
@pytest.mark.parametrize('breed_name', breeds_main)
# @pytest.mark.parametrize('breed_name', ['toy terrier'])
def test_random_image_by_breed(base_url, breed_name):
    res = requests.get(base_url + "/api/breed/" + breed_name + "/images/random")
    assert res.status_code == 200

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


# получение нескольких случайных картинок по основной породе
# TODO найти, как сделать случайный выбор параметра из списка, чтобы не прогонять все породы
# @pytest.mark.parametrize('breed_name', breeds_main)
@pytest.mark.parametrize('breed_name', ['hound'])
@pytest.mark.parametrize('count_images', ['1', '50', '100'])
def test_some_random_image_schema_by_breed(base_url, count_images, breed_name):
    res = requests.get(base_url + "/api/breed/" + breed_name + "/images/random/" + count_images)
    assert res.status_code == 200

    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "array"},
            "status": {"type": "string"},
        },
        "required": ["message", "status"]
    }

    validate(instance=res.json(), schema=schema)


# получение случайной картинки по полной породе
# TODO найти, как сделать случайный выбор параметра из списка, чтобы не прогонять все породы
# @pytest.mark.parametrize('breed', breeds_main)
@pytest.mark.parametrize('breed', ['terrier'])
def test_random_image_by_breed(base_url, breed):
    res = requests.get(base_url + "/api/breed/" + breed + "/images/random")
    assert res.status_code == 200

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


# получение нескольких случайных картинок по основной породе
# TODO найти, как сделать случайный выбор параметра из списка, чтобы не прогонять все породы
@pytest.mark.parametrize('breed_name', breeds_main)
# @pytest.mark.parametrize('breed_name', ['terrier'])
@pytest.mark.parametrize('count_images', ['1', '50', '100'])
def test_some_random_image_schema(base_url, count_images, breed_name):
    res = requests.get(base_url + "/api/breed/" + breed_name + "/images/random/" + count_images)
    assert res.status_code == 200

    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "array"},
            "status": {"type": "string"},
        },
        "required": ["message", "status"]
    }

    validate(instance=res.json(), schema=schema)
