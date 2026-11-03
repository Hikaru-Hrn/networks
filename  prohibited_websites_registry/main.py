import re
import sys


# Регулярное выражение для URL
URL_PATTERN = re.compile(
    r"^https?://"  # http:// https://
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # Домен
    r"localhost|"  # Либо localhost
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # Либо IPv4-адрес
    r"(?::\d{1,5})?"  # Опциональный порт: :80, :8080
    r"(?:/?|[/?]\S+)$",  # Опциональный путь
    re.IGNORECASE,
)


def check_input_url(url: str) -> bool:
    if not isinstance(url, str):
        return False
    return bool(URL_PATTERN.match(url.strip()))

user_URL = input("Enter your URL: ")
if not(check_input_url(user_URL)):
    sys.exit("Invalid URL")

with open("register.txt", "r") as file:
    for line in file:
        if user_URL in line:
            print(f"Url {user_URL} in register!")

