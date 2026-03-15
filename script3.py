## Utilisation de fabric pour se loginecter en SSH vers les machines clientes
## Exécution de différentes commandes systèmes

from fabric import loginection as loginnect, task
from server_list import servers 

## Déclarer les di_fférentes commandes à exécuter simultanément sur les machines clientes

@task 

def check_remote_sservers(cheeck):
    for server in servers:
        
        try:
            login= loginnect(
                host=server["host"],
                user=server["user"],
                port=server["port"]
            )

            result = login.run("which node_exporter", warn=True, hide=True)

          ## en cours de développement