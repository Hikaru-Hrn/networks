import pytest
from main import check_input_url

def test_right_urls():
    assert check_input_url('https://www.google.com') == True
    assert check_input_url('https://google.com') == True
    assert check_input_url('https://gosuslugi.ru') == True
    assert check_input_url('https://yandex7123.ru') == True
    assert check_input_url('https://www.yandex.com/') == True

def test_wrong_urls():
    assert check_input_url('htt//google.com') == False
    assert check_input_url('https://google') == False
    assert check_input_url('https:/google.com') == False
    assert check_input_url('') == False
    assert check_input_url('Vasya') == False
