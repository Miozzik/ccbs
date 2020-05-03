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
