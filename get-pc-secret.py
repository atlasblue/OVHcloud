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

# Replace with your actual cluster service name
service_name = "cluster-xxxx.nutanix.ovh.net"

# Get list of servers
try:
    cluster_info = client.get(f"/nutanix/{service_name}")
    nodes = cluster_info.get("targetSpec", {}).get("nodes", [])
except Exception as e:
    print(f"Error to fetech servers configuration : {e}")
    nodes = []

# For each server check and get the password
for node in nodes:
    server_name = node.get("server")
    if not server_name:
        continue

    try:
        # Check if a password is available
        secrets = client.post(f"/dedicated/server/{server_name}/authenticationSecret")
        password_uuid = secrets[0].get("password") if secrets else None
        if password_uuid:
            # Get the password using password uuid
            password_info = client.post("/secret/retrieve", id = password_uuid)
            print(password_uuid)
            print(f"🔐 Server: {server_name} | Password: {password_info.get('secret')}")
        else:
            print(f"🔒 Server: {server_name} | No password available")

    except Exception as e:
        print(f"⚠️ Error with server {server_name} : {e}")
