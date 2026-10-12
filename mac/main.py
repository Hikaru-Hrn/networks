import re
def is_valid_mac(mac):
    # Шаблон для формата XX:XX:XX:XX:XX:XX или XX-XX-XX-XX-XX-XX
    pattern = r"^(?:[0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}$"

    # re.match проверяет соответствие с начала строки
    if re.match(pattern, mac):
        return True
    raise ValueError("Invalid MAC address")

user_mac = input("Enter your mac address (format - F0-79-59-70-A7-20): ").upper()

is_valid_mac(user_mac)


mac = (
    user_mac.replace(' ', '')
    .replace('.', '')
    .replace('-', '')
    .replace('—', '')
)[:6]

with open("mac/mac-vendor.txt", "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith(mac):
            line = line.split("\t")
            print(f"Your mac address: {user_mac}, your mac manufacturer: {line[1]}")
            exit(0)
    print("Invalid MAC address")
