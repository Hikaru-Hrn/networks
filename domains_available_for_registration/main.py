import json
import re
import time
import random
import requests

# Имя твоего файла из архива
DUMP_FILE = "domains"
OUTPUT_CLEAN_DOMAINS = "extracted_domains.txt"
OUTPUT_FREE_DOMAINS = "available_domains.txt"

# Сколько свободных доменов найти до остановки
TARGET_FREE_COUNT = 15

# Регулярка для чистых доменов 2-го уровня в популярных зонах (.ru, .com, .org, .net, .info, .su, .biz, .top, .site)
# Исключаем IP-адреса и поддомены 3-го уровня (типа 0-00.lordfilm0.biz)
DOMAIN_2ND_LEVEL_RE = re.compile(
    r"^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]\.(ru|com|org|net|info|su|biz|top|site|online|club|pro|xyz|fun)$"
)


def load_and_filter_domains(filepath: str) -> list[str]:
    print(f"[*] Загружаем {filepath} ...")
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        raw_list = json.load(f)

    print(f"[*] Всего записей в файле: {len(raw_list)}")

    clean_domains = set()
    for item in raw_list:
        if not isinstance(item, str):
            continue
        # Убираем лишние пробелы, кавычки (в начале файла есть \"certr.ru) и www.
        d = item.strip().strip('"').strip("'").strip("\\").lower()
        if d.startswith("www."):
            d = d[4:]

        # Проверяем, что это валидный домен 2-го уровня, а не поддомен или IP
        if DOMAIN_2ND_LEVEL_RE.match(d):
            clean_domains.add(d)

    result = sorted(clean_domains)
    print(f"[+] Отобрано уникальных доменов 2-го уровня: {len(result)}")
    return result


def is_domain_available(domain: str) -> bool:
    """
    Проверяет доступность домена для регистрации через API http://api.whois.vu/
    """
    url = f"http://api.whois.vu/?q={domain}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            # Явный ответ от API, что домен свободен и не зарезервирован
            if data.get("available") == "yes":
                return True
    except Exception as e:
        print(f"  [!] Ошибка запроса для {domain}: {e}")
    return False


def main():
    # 1. Загружаем и фильтруем домены второго уровня из JSON-выгрузки
    domains = load_and_filter_domains(DUMP_FILE)
    if not domains:
        print("[-] Не удалось найти подходящие домены.")
        return

    with open(OUTPUT_CLEAN_DOMAINS, "w", encoding="utf-8") as f:
        f.write("\n".join(domains))
    print(f"[*] Отфильтрованный список сохранен в {OUTPUT_CLEAN_DOMAINS}")

    # Перемешиваем, чтобы не идти только по доменам на цифру '0' и '1'
    random.shuffle(domains)

    # Очищаем файл результатов перед стартом
    open(OUTPUT_FREE_DOMAINS, "w", encoding="utf-8").close()

    # 2. Проверяем через WHOIS API
    free_domains = []
    print(f"\n[*] Ищем первые {TARGET_FREE_COUNT} свободных для покупки доменов...\n")

    for idx, domain in enumerate(domains, start=1):
        available = is_domain_available(domain)
        status = "СВОБОДЕН!" if available else "занят"
        print(f"[{idx}] {domain:<35} -> {status}")

        if available:
            free_domains.append(domain)
            with open(OUTPUT_FREE_DOMAINS, "a", encoding="utf-8") as f:
                f.write(domain + "\n")

            if len(free_domains) >= TARGET_FREE_COUNT:
                print(f"\n[+] Найдено {TARGET_FREE_COUNT} свободных доменов! Поиск завершен.")
                break

        # Пауза 0.6 сек, чтобы не словить бан от api.whois.vu
        time.sleep(0.6)

    print("\n=== СВОБОДНЫЕ ДОМЕНЫ ДЛЯ ПРОВЕРКИ НА REG.RU / NIC.RU ===")
    for d in free_domains:
        print(d)
    print(f"\nСписок также сохранен в {OUTPUT_FREE_DOMAINS}")


if __name__ == "__main__":
    main()