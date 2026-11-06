import re
import sys
import socket

# Регулярное выражение для URL
URL_PATTERN = re.compile(
    r"^https?://"  # http:// https://
    r"((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # Домен
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

def check_url_in_register(user_URL: str):
    domain = URL_PATTERN.match(user_URL.strip()).group(1)
    try:
        ip = socket.gethostbyname(domain)
    except socket.gaierror:
        ip = None
        print(f"Could not determine the IP for the domain {domain}")

    with open("register.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            line_el = line.split(";")

            urls_in_line = line_el[1].split(",")
            domains_in_line = line_el[2].split(",")
            ips_in_line = line_el[3].split(",")

            if user_URL in urls_in_line or domain in domains_in_line or ip in ips_in_line:
                print(f"Url {user_URL} in register!")
                print(f"ip: {ip}")
                break
        else:
            print(f"Domain not found in the registry {domain}")


user_URL = input("Enter your URL: ")
if not(check_input_url(user_URL)):
    sys.exit("Invalid URL")

check_url_in_register(user_URL)