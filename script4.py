## INFORRMATION RELATIVE AUX DIFFERENTES MACHINES CLIENTES
## PROJET N COURS DE DEVELOPPEMENT

## UTILISTTION DU MODULE FABRIC -----  ThreadingGroup

from server_list import servers
from fabric import ThreadingGroup as Group 
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
    "sudo apt install prometheus-node-exporter -y",
    "sudo systemctl start node_exporter",
    "sudo systemctl status node_exporter"
]

## Préparation del'inventaire

host_server_list = []
for h in servers:
    host = h.get("host")
    user = h.get("user")
    port = h.get("port",22)

    if host and user:
        host_server_list.append(f"{user}@{host}:{port}")
    else:

        logging.warning(f"wrong entry on {h}, please,try again")
         

## exécution de différentes commandes de manière simultané avec gestion d'erreur
# GESTION D'ERREUR  AVEC  TRY EXCEPT 

def cmd_run(group, command):

    if not command:
        logging.warning(" Please no command found, Go to the next...")
        return

    try:

        if command.startswith("sudo"):

            results = group.sudo(command[5:].lstrip(), hide=True, warn=True, pty=True)
        else:
            results = group.run(command, hide=True, warn=True, pty=True)
            
        # Analyse du résultat pour chaque serveur du groupe et exécution simultanée

        for connection, result in results.items():

            if result.ok:
                logging.info(f"[{connection.host}] SUCCESS : {command}")
                logging.debug(f"Sortie : {result.stdout.strip()}")
            else:
                logging.error(f"[{connection.host}] FAILED : {command}")
                logging.error(f"Erreur : {result.stderr.strip()}")

    except Exception as e:
        logging.exception(f"Erreur critique lors de l'exécution de '{command}': {e}")
    
    ## Execution finale
if __name__ == "__main__":

    if not host_server_list:
        logging.critical("Aucun serveur valide dans server_list.py.")
        exit(1)

    logging.info(f"Démarrage du déploiement sur {len(host_server_list)} serveurs.")

    try:
        # création du group ssh via ssh-keygen -t ed25519
        my_group = Group(*host_server_list, connect_kwargs={"key_filename": "path-pr-key"})

        for cmd in remote_commands:
            logging.info(f"=== EXECUTION : {cmd} ===")
            cmd_run(my_group,cmd)
            
        logging.info("Processus de déploiement terminé.")

    except Exception as global_err:
        logging.critical(f"Impossible d'initialiser le groupe de serveurs : {global_err}")





    

