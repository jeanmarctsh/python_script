## Utilisation de fabric pour se connecter en SSH vers les machines clientes
## Exécution de différentes commandes systèmes

from fabric import Connection as connnect, task
from server_list import servers 

## Renseignement de différentes commandes à exécuter simultanément au niveau des machines clientes

from fabric import Connection, task
from server_list import servers

remote_commands = [
    "ip a | grep ens",
    "sudo apt update",
    "sudo apt-cache policy prometheus-node-exporter",
    "sudo apt install node_exporter-1.10.2.linux-amd64 -y",
    "sudo systemctl start node_exporter",
    "sudo systemctl status node_exporter"
]

@task
def login_run(c):

    for server in servers:

        host = server.get("host")
        user = server.get("user")
        port = server.get("port", 22)

        if host and user:

            try:
                print(f"\nConnexion vers {host} avec l'utilisateur {user}")

                con = Connection (
                    host=host,
                    user=user,
                    port=port,
                    connect_kwargs={ "key_filename":  ####### ssh private key-path 
                             }
                 )

                for cmd in remote_commands:
                    print(f"Exécution de : {cmd}")
                    if cmd.startswith("sudo"):
                        result = con.sudo(cmd.replace("sudo ", ""), hide=False)
                    else:
                        result = con.run(cmd, hide=False)
                    print(result.stdout)

            except Exception as e:
                print(f"Impossible de se connecter à {host}: {e}")

        else:
            print(f"Veuillez renseigner correctement les informations pour : {server}")


    ## refaire calmement pour une bonne exécution