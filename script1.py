from pathlib import Path
import shutil
import os
import tarfile
import requests
import subprocess

# Path declaration

home = Path.home()
folder_work = "devops_pyt"
full_path = home / folder_work
path_file_destination = "/usr/local/bin"
file_name = "node_exporter-1.10.1.linux-amd64.tar.gz"
folder_save = full_path / "extract_folder_name"
extract_folder_name = "zip"
finale_working_directory = home / folder_work / file_name

## check if file exist in the folder (full_path)

if finale_working_directory.exists():
    print(f"le fichier {file_name} existe dans {full_path}")
else:
    print(f"le fichier {file_name} n'existe pas  dans {full_path} veuillez le télécharger svp")

## setup url and download file

URL = "https://github.com/prometheus/node_exporter/releases/download/v1.10.1/node_exporter-1.10.1.linux-amd64.tar.gz"

response = requests.get(URL, stream=True)
if response.status_code==200:
    with open(file_name, 'wb') as file:
        with open(file_name, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
else:
    print("file_Download failed")

## check if folder zip exist

if extract_folder_name.exists():
    print(f"le dossier {extract_folder_name} existe dans {full_path}")

## create the folder
else:

    print(f"le dossier {extract_folder_name} n'existe pas dans {full_path} veuillez le créer")
    extract_folder_name.mkdir(parents=True, exist_ok=True)
    print(f"le dossier {extract_folder_name} a été crée correctement.")

## extraction du fichier et envoi dans le dossier 

with tarfile.open(extract_folder_name, 'r:gz') as f_e:
    f_e.extractall(path=extract_folder_name)
    #f_e.list()


## acceder au dossier maintenant 

os.chdir(path=extract_folder_name)

## check if file exist in the destination folder before make a copy

for dir in path_file_destination.itedir():
    if dir == file_name and dir.is_file():
        print(f"le fichier {dir} a été trouvé")

        break
    else:
        print(f"le fichier {dir} n'a pas été trouvé")
        shutil.copy(src=file_name, dst=dir)
        print(f"le fichier {file_name} a été copié avec succès")


## création d'un user de service avec le module subprocess


