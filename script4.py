## INFORRMATION RELATIVE AUX DIFFERENTES MACHINES CLIENTES
## PROJET N COURS DE DEVELOPPEMENT

## UTILISTTION DU MODULE FABRIC -----  ThreadingGroup

from server_list import servers
from fabric import ThreadingGroup as Grouup 
import logging
from pathlib import Path


## utilisation du module Pathlib pour créer le dossier qui n'existe pas encore.

# 1. Fixation du chemin et le rendre flexible

BASE_DIR = Path(__file__).resolve().parent

# 2. Mise en place et création du dossier LOG

LOG_DIR = BASE_DIR / "logs"

#  3. CREATION DU DOSSIER

LOG_DIR.mkdir(exist_ok=True)

# CREATION DU CHEMIN POUR LE FICHIER log_app.log

LOG_FILE =  LOG_DIR / "log_app.log"

## Configuration des paramètres pour le module python logging

logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s",
    handlers=  [

        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]  )



## Commandes qui seront exécutées simultanément sur les machines clientes

remote_commands = [
    "ip a | grep ens",
    "sudo apt update",
    "sudo apt-cache policy prometheus-node-exporter",
    "sudo apt install node_exporter-1.10.2.linux-amd64 -y",
    "sudo systemctl start node_exporter",
    "sudo systemctl status node_exporter"
]

host_server_list = []

for h in servers:
    host = h.get("host")
    user = h.get("user")
    port = h.get("port",22)

    if host and user:
        host_server_list.append(f"{user}@{host}:{port}")
    else:

        logging.warning(f"bad value on {h}")
        print(logging.warning("not connected"))

group = Grouup(*host_server_list, connect_kwargs={"key_filename": "path-to-key"})

## exécution de différentes commandes de manière simultané avec gestion d'erreur
# GESTION D'ERREUR  AVEC  TRY EXCEPT 

try:

    pass


except:

    pass

