
# Install the latest release of the OVH Python wrapper before running 
# pip install ovh

import json
import ovh

# Instantiate an OVH Client.
# You can generate new credentials with full access to your account on
# the token creation page (https://api.ovh.com/createToken/index.cgi?GET=/*&PUT=/*&POST=/*&DELETE=/*)
client = ovh.Client(
	endpoint='ovh-xx',               # Endpoint of API OVH (List of available endpoints: https://github.com/ovh/python-ovh#2-configure-your-application)
	application_key='',    # Application Key
	application_secret='', # Application Secret
	consumer_key='',       # Consumer Key
)

# Define the variables that configure your cluster redeployment
service_name = "cluster-3517.nutanix.ovh.net" # The identifier of the Nutanix cluster
erasure_coding = False # A boolean flag whether erasure coding is enabled.
infra_vlan_number = 0 # The infrastructure VLAN number to use 
nodes = [ 
    {"ahvIp": "192.168.10.21", "cvmIp": "192.168.10.1"}, # Hypervisor and CVM IP Node1
    {"ahvIp": "192.168.10.22", "cvmIp": "192.168.10.2"}, # Hypervisor and CVM IP Node2
    {"ahvIp": "192.168.10.23", "cvmIp": "192.168.10.3"}, # Hypervisor and CVM IP Node3
]
prism_element_vip = "192.168.10.10" # Cluster VIP
prism_central = {       
    "vip": "192.168.10.30",   # Prism Central IP
    "size": "large",          # Prism Central size Allowed: large┃small┃xlarge┃xsmall
    "type": "alone"           # Prism Central Type Allowed: alone┃scale
}
redundancy_factor = 2 # RF values Allowed 2┃3 
version = "7.3.0.5"   # AOS version use available versions using get-versions.py 
gateway_cidr = "192.168.10.254/24" # Internal Gateway IP with mask

# Perform the API call (HTTP PUT) to redeploy the cluster service.
# The URL path includes the service_name and the query-parameters (redeploycluster, scaleOut).
try:
    result = client.put(f"/nutanix/{service_name}?redeploycluster=true&scaleOut=false",
        erasureCoding=erasure_coding,
        infraVlanNumber=infra_vlan_number,
        nodes=nodes,
        prismElementVip=prism_element_vip,
        prismCentral=prism_central,
        redundancyFactor=redundancy_factor,
        version=version,
        gatewayCidr=gateway_cidr
    )
    # Print the result from the API, nicely formatted as JSON.
    status = result.get("status")
    print(json.dumps(status, indent=4))
except ovh.exceptions.APIError as e:
    print(f"API Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")