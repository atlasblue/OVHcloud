import ovh
import json

# Instantiate an OVH Client.
# You can generate new credentials with full access to your account on
# the token creation page (https://api.ovh.com/createToken/index.cgi?GET=/*&PUT=/*&POST=/*&DELETE=/*)
client = ovh.Client(
	endpoint='ovh-xx',     # Endpoint of API OVH (List of available endpoints: https://github.com/ovh/python-ovh#2-configure-your-application)
	application_key='',    # Application Key
	application_secret='', # Application Secret
	consumer_key='',       # Consumer Key
)

# Numéro du cluster
cluster_number = "3517"
cluster_id = f"cluster-{cluster_number}.nutanix.ovh.net"

# Étape 1 : Récupérer la liste des serveurs
try:
    cluster_info = client.get(f"/nutanix/{cluster_id}")
    nodes = cluster_info.get("targetSpec", {}).get("nodes", [])
except Exception as e:
    print(f"Erreur lors de la récupération du cluster : {e}")
    nodes = []

# Étape 2 : Pour chaque serveur, vérifier et récupérer le mot de passe
for node in nodes:
    server_name = node.get("server")
    if not server_name:
        continue

    try:
        # Vérifie si un mot de passe est disponible
        secrets = client.post(f"/dedicated/server/{server_name}/authenticationSecret")
        password_uuid = secrets[0].get("password") if secrets else None
        if password_uuid:
            # Récupère le mot de passe via l'UUID
            password_info = client.post("/secret/retrieve", id = password_uuid)
            print(password_uuid)
            print(f"🔐 Server: {server_name} | Password: {password_info.get('secret')}")
        else:
            print(f"🔒 Server: {server_name} | No password available")

    except Exception as e:
        print(f"⚠️ Error with server {server_name} : {e}")