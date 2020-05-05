import os
import re
import paramiko
import time
import getpass
import tempfile
from datetime import date


if not os.path.isdir("Backup"):
    os.mkdir("Backup")
os.chdir("Backup")
current_date = str(date.today())
if not os.path.isdir(current_date):
    os.mkdir(current_date)
os.chdir("..")

open_client_list = open("client_list.txt", encoding="utf-8").readlines()

if len(open_client_list) < 22:
    ssh_user = input("Логин SSH: ")
    ssh_password = getpass.getpass("Пароль SSH: ")
    enable_password = getpass.getpass("Пароль Пароль для enable: ")


for readoneline in open_client_list:
    readoneline = readoneline.strip()
    if len(readoneline) > 21:
        address, port = re.search(r"(\d+.\d+.\d+.\d+|\S+[a-zA-Z]):*(\d*)", readoneline).group(1, 2)
        device_name = re.search(r'(\d+.\d+.\d+.\d+|\S+[a-zA-Z]):*\d*.+"(.*)"', readoneline).group(2)
        if not len(device_name):
            device_name = address
        enable_password = re.search(r"enable: (\S*)", readoneline).group(1)
        ssh_user, ssh_password = re.search(r'.+\s(\w+):(\S+)', readoneline).group(1, 2)
        print(f"Подключаемся к: {device_name}")
    else:
        address, port = readoneline.split(":")
        print(f"Подключаемся к: {address}")


    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    client.connect(
        hostname=address,
        username=ssh_user,
        password=ssh_password,
        look_for_keys=False,
        allow_agent=False)
    with client.invoke_shell() as ssh:
        ssh.send('enable\n')
        ssh.send(enable_password + '\n')
        time.sleep(0.5)
        ssh.send('terminal length 0\n')
        time.sleep(0.5)
        ssh.recv(1000)
        ssh.send('show startup-config\n')
        time.sleep(0.5)
        result = ssh.recv(10000).decode('utf-8')
    with tempfile.NamedTemporaryFile(mode='w+') as temp_file:
        temp_file.write(result)
        temp_file.seek(0)

        os.chdir("Backup")
        os.chdir(current_date)

        hostname = re.findall(r"hostname (\S*)", temp_file.read())[0]

        temp_file.seek(0)

        with open(hostname, "w", encoding="utf-8") as result_file:
            for i in temp_file.readlines()[1:-1]:
                if not i.startswith("!") and not i.startswith("\n"):
                    result_file.write(i)

        temp_file.write("")
        temp_file.seek(0)
        print(f"Устройство {hostname} готово")
        os.chdir("..")
        os.chdir("..")
else:
    print("Готово :)")
