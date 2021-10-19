import pytest
import requests


def pytest_addoption(parser):
    parser.addoption(
        "--url",
        # default="https://ya.ru",
        default="https://dog.ceo"
    )

    parser.addoption(
        "--status_code",
        default=200,
        # choices=["get", "post", "put", "patch", "delete"],
    )


@pytest.fixture
def base_url(request):
    return request.config.getoption("--url")
