import os
import re
import paramiko
from datetime import date

# Создаём директорию для бэкапа
def create_folder(dirname=None):
    if not os.path.isdir("Backup"):
        os.mkdir("Backup")
    os.chdir("Backup")
    current_date = str(date.today())
    if dirname and not os.path.isdir(dirname):
        os.mkdir(dirname)
    elif dirname==None and not os.path.isdir(current_date):
        os.mkdir(current_date)
    os.chdir("..")
    return print("Папка подготовлена")


create_folder()


open_client_list = open("client_list.txt", encoding="utf-8").readlines()
# Получаеи нужные данные
for readoneline in open_client_list:
    readoneline = readoneline.strip()
    ip, port = re.search(r"(\d+.\d+.\d+.\d+|\S+[a-zA-Z]):*(\d*)", readoneline).group(1, 2)
    device_name = re.search(r'(\d+.\d+.\d+.\d+|\S+[a-zA-Z]):*\d*.+"(.*)"', readoneline).group(2)
    if not len(device_name):
        device_name = "Устройство с НЕ заданым названием"
    find_enable_password = re.search(r"enable: (\S*)", readoneline).group(1)
    ssh_ip, ssh_password = re.search(r'.+\s(\w+):(\S+)', readoneline).group(1, 2)
    