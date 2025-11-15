import json
import ovh

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
service_name = "cluster-3517.nutanix.ovh.net"

# Fetch current cluster configuration
try:
    result = client.get(f"/nutanix/{service_name}")
    print(json.dumps(result, indent=4))
except ovh.exceptions.APIError as e:
    print(f"API Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")