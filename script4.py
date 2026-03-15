## INFORRMATION RELATIVE AUX DIFFERENTES MACHINES CLIENTES
## PROJET N COURS DE DEVELOPPEMENT

from server_list import servers
from fabric import ThreadingGroup as Grouup

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

group = Grouup(*host_server_list, connect_kwargs={"key_filename": "path-to-key"})

## exécution de différentes commandes en même temps
for apt in remote_commands:
    print(f"\n=== Exécution de : {apt} ===")
    if apt.startswith("sudo"):
        group.sudo(apt.replace("sudo ", ""), hide=False)
    else:
        group.run(apt, hide=False)