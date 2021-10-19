import pytest
import requests


@pytest.fixture
def base_url(request):
    return request.config.getoption("--url")


@pytest.fixture
def status_code(request):
    return request.config.getoption("--status_code")


def test_url_status(base_url, status_code):
    target = base_url + f"/status/{status_code}"
    response = requests.get(url=target)
    assert response.status_code == int(status_code)
