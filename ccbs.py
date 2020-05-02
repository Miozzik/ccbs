import os
from datetime import date

# Создаём директорию для бэкапа
def create_folder():
    if os.path.isdir("Backup"):
        pass
    else:
        os.mkdir("Backup")
    os.chdir("Backup")
    current_date = str(date.today())
    os.mkdir(current_date)
    return True
