#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['stable'],
    'supported_by': 'Guy'
}

DOCUMENTATION = '''
---
module: rancher_vsphere_node_template

short_description: This module handles managing rancher node templates

version_added: "1.0"

description:
    - "This module creates node templates in a given rancher install. Currently it will only deal with whether a named node template exists (creating it if it doesn't). In the future it should be expanded to check the properties of the returned node template and perform updates."

options:
    api_bearer_token:
        description:
            - The rancher bearer token to authenticate with 
        required: true
    cloud_config:
        description:
            -  Specify the cloud-config YAML script as a single line. The correct YAML indentation must be maintained and \n used at the end of each line. See https://cloudinit.readthedocs.io/en/latest/topics/examples.html
        required: false
    clone_from:
        description:
            -  The path to the image to build the VM from, e.g. /SDDC-Datacenter/vm/Templates/bastion-plus-cloud-init
        required: flase    
    cloud_init:
        description:
            -   Need to send only ""
        required: true
    cloud_credential_id:
        description:
            -  The ID of the Cloud Credentials that have been set-up within the Rancher web UI for your vCenter server, e.g. cattle-global-data:cc-jg2xh
        required: true
    content_library:
        description:
            -  The name of the vSphere content library that contains the template to build the VM from.
        required: false
    cpu_count:
        description:
            -  The number of CPUs to assign to the VM
        required:
    creation_type:
        description:
            -  The type of creation method to use: 'template' (default) if using a template from the datacentre, 'library' 
               if using a vSphere content library, 'vm' if cloning an existing VM or 'legacy' if installing from a boot2docker ISO image
        required: true
    custom_attribute:
        description:
            -  Used to attach metadata to objects in the vSphere inventory to make it easier to sort and search for these objetcs.
        required: false
    datacentre:
        description:
            -  The name of the data centre in vCentre to build the VM on, e.g. /SDDC-Datacenter
        required: true
    datastore:
        description:
            -  The datastore to create the VM disk on, e.g. /SDDC-Datacenter/datastore/WorkloadDatastore
        required: true 
    datastore_cluster:
        description:
            -  The name of the datastore cluster to allocate storge space from.
        required: Only required when multiple datastore cluster have been configured on a multi-host cluster.
    disk_size:
        description:
            -  The size of the disk to create and attach to the VM in MB
        required: true
    engine_install_url:
        description:
            -  The URL of the script that install docker. e.g. https://releases.rancher.com/install-docker/19.03.sh
        required: false
    folder:
        description:
            -  The path to the folder to create the VM in. This must already exist in the datacenter, e.g. /SDDC-Datacenter/vm
        required: true
    hostsystem:
        description:
            -  The ESXi host to create the VM on. Blank if only one ESXi host in the cluster or if using ditributed resource management (DRM).
        required: false
    insecure_registries:
        description:
            -  The FQDN of any insecure resigtry to be used
        required: false
    memory_size:
        description:
            -  The amount of RAM to allocate to VMs in MB
        required: true
    name:
        description:
            -  The name of the node template to create/update
        required: true
    network:
        description:
            -  The name of the existing network to connect the VM to, e.g. /SDDC-Datacenter/network/Subnet_Internet_access
        required: true
    node_taints:
        description:
            -  Taints are used to influence/define the ESXi host chosen when a VM is created or moved. 
               The key-name, key-value and effect ('NoSchedule', 'NoExecute' or 'PreferNoSchedule')
        required: false    
    pool:
        description:
            -  The resource pool to create the VM in, e.g. /SDDC-Datacenter/host/Cluster-1/Resources/Compute-ResourcePool
        required: false
    rancher_domain:
        description:
            - The Name of the rancher domain. ### Note sure we need this.
        required: true
    ssh_password:
        description:
            -  This is a legacy field and not required.
        required: true
    ssh_port:
        description:
            -  This is a legacy field and not required.
        required: true
    ssh_user:
        description:
            -  This is a legacy field and not required.
        required: true
    ssh_user_group:
        description:
            -  This is a legacy field and not required.
        required: true
    username:
        description:
            -   This was "" in the working post message.
        required: false
    use_internal_ip_address:
        description:
            -  Set to True so that the internal ports between VM instances are open to each other.
        required: true
    vcenter:
        description:
            -  FQDN of the VCentre server. Note: This was "" in the working post message.
        required: true
    vcenter_port:
        description:
            -  Port to communicate with the vSphere API (443)
        required: true
    vsphere_config_param:
        description:
            -  Configuration Parameters used for guestinfo
        required: false

author:
    - Guy
'''

EXAMPLES = '''
- name: Rancher vSphere Node Template Centos 7
  rancher_vsphere_node_template:
	api_bearer_token: token_export
	cloud_config: "#cloud-config\nruncmd:\n - [ sh, -xc, \"echo $(date) ': hello world!'" ]"
    clone_from: "/SDDC-Datacenter/vm/Templates/bastion-plus-cloud-init"
    cloud_credential_id: XXXXXXXXXXXXXX
	cpu_count: 2
	creation_type: template
	datacentre: "/SDDC-Datacenter"
	datastore: "/SDDC-Datacenter/datastore/WorkloadDatastore"
	datastore_cluster:              # Only required for multi-node ESXi platform
	disk_size: 81920
	engine_install_url: https://releases.rancher.com/install-docker/19.03.sh
	folder: "/SDDC-Datacenter/vm"
	insecure_registries: 
      - harbor.cloudranger.co.uk:80
	memory_size: 8192
    name: "My vSphere Node Template"
	network: 
       - /SDDC-Datacenter/network/Subnet_Internet_access
	pool: "/SDDC-Datacenter/host/Cluster-1/Resources/Compute-ResourcePool"
    rancher_domain: rancher.d2.cloudranger.co.uk
	use_internal_ip_address: true
	vcenter_port: 443
	vsphere_config_param: 
      - disk.enableUUID=TRUE
'''

RETURN = '''
node_template_id:
    description: The unique identifier for the node template
    type: string
'''

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url, url_argument_spec
import json


class RancherVsphereNodeTemplate(object):
    def __init__(self):
        self.module_spec = url_argument_spec()
        self.module_spec.update(
            api_bearer_token=dict(type='str', required=True),
            cloud_config=dict(type='str', default='#cloud-config'),
            clone_from=dict(type='str', required=False),
            cloud_init=dict(type='str', default=""),
            cloud_credential_id=dict(type='str', required=True),
            content_library=dict(type='str', required=False),
            cpu_count=dict(type='int', default='2'),
            creation_type=dict(type='str', default='template'),
            custom_attribute=dict(type='str', required=False),
            datacentre=dict(type='str', required=True),
            datastore=dict(type='str', required=True),
            datastore_cluster=dict(type='str', required=False),
            disk_size=dict(type='int', default='81920'),
            engine_install_url=dict(type='str', required=True),
            folder=dict(type='str', required=True),
            hostsystem=dict(type='str', required=False),
            insecure_registries=dict(type='list', elements='str', default=[]),
            memory_size=dict(type='int', default='2048'),
            name=dict(type='str', required=True),
            network=dict(type='list', elements='str', default=[]),
            pool=dict(type='str', required=True),
            rancher_domain=dict(type='str', required=True),
            ssh_password=dict(type='str', required=True, no_log=True),
            ssh_port=dict(type='int', default='22'),
            ssh_user=dict(type='str', default='docker'),
            ssh_user_group=dict(type='str', default='staff'),
            tags=dict(type='list', elements='str', default=[]),
            username=dict(type='str', required=False),
            use_internal_ip_address=dict(type='bool', default=True),
            vapp_property=dict(type='list', elements='str', required=False, default=[]),
            vcenter=dict(type='str', required=False),
            vcenter_port=dict(type='int', default='443'),
            vapp_ip_allocation_policy=dict(type='str', required=False, default=''),
            vapp_ip_protocol=dict(type='str', required=False, default=''),
            vapp_transport=dict(type='str', required=False, default=''),
            vsphere_config_param=dict(type='list', elements='str', default=[]),
        )

        # Module input variables
        self.api_bearer_token = None
        self.cloud_config = None
        self.clone_from = None
        self.cloud_init = None
        self.cloud_credential_id = None
        self.content_library = None
        self.cpu_count = None
        self.creation_type = None
        self.custom_attribute = None
        self.datacentre = None
        self.datastore = None
        self.datastore_cluster = None
        self.disk_size = None
        self.engine_install_url = None
        self.folder = None
        self.hostsystem = None
        self.insecure_registries = None
        self.memory_size = None
        self.name = None
        self.network = None
        self.pool = None
        self.rancher_domain = None
        self.ssh_password = None
        self.ssh_port = None
        self.ssh_user = None
        self.ssh_user_group = None
        self.tags = None
        self.username = None
        self.use_internal_ip_address = None
        self.vapp_property = None
        self.vcenter = None
        self.vcenter_port = None
        self.vapp_ip_protocol = None
        self.vapp_ip_allocation_policy = None
        self.vapp_transport = None
        self.vsphere_config_param = None

        # Internal variables that aren't set through the module input
        self.path = '/v3/nodeTemplates/'

        self.results = dict(
            changed=False,
            node_template_id='',
        )

        self.module = AnsibleModule(
            argument_spec=self.module_spec,
            supports_check_mode=True
        )

        res = self.exec_module(**self.module.params)
        self.module.exit_json(**res)

    def exec_module(self, **kwargs):
        for key in list(self.module_spec.keys()):
            setattr(self, key, kwargs[key])

        node_template_id = self.template_exists()

        if node_template_id is False:
            self.create_template()
        else:
            self.results['node_template_id'] = node_template_id

        return self.results

    def create_template(self):
        headers = {
            'Authorization': 'Bearer ' + self.api_bearer_token,
            'Content-Type': 'application/json'
        }

        request_type = 'POST'

        data = {
            "name": self.name,
            "vmwarevsphereConfig": {
                "boot2dockerUrl": "",
                "cfgparam": self.vsphere_config_param,
                "cloneFrom": self.clone_from,
                "cloudConfig": self.cloud_config,
                "cloudinit": self.cloud_init,
                "contentLibrary": self.content_library,
                "cpuCount": self.cpu_count,
                "creationType": self.creation_type,
                "customAttribute": self.custom_attribute,
                "datacenter": self.datacentre,
                "datastore": self.datastore,
                "datastoreCluster": self.datastore_cluster,
                "diskSize": self.disk_size,
                "folder": self.folder,
                "hostsystem": self.hostsystem,
                "memorySize": self.memory_size,
                "network": self.network,
                "pool": self.pool,
                "sshPassword": self.ssh_password,
                "sshUser": self.ssh_user,
                "sshUserGroup": self.ssh_user_group,
                "tag": self.tags,
                "username": self.username,
                "vappIpallocationpolicy": self.vapp_ip_allocation_policy,
                "vappIpprotocol": self.vapp_ip_protocol,
                "vappProperty": self.vapp_property,
                "vappTransport": self.vapp_transport,
                "vcenter": self.vcenter,
                "vcenterPort": self.vcenter_port,
            },
            "useInternalIpAddress": self.use_internal_ip_address,
            "cloudCredentialId": self.cloud_credential_id,
            "engineInsecureRegistry": self.insecure_registries,
            "engineInstallURL": self.engine_install_url,
        }

        resp, info = fetch_url(self.module, self.rancher_domain + self.path, data=json.dumps(data), headers=headers,
                               method=request_type)

        if info["status"] != 201:
            print(info);exit()
            reason = 'Rancher gave a status code of ' + str(info["status"]) + ' creating vsphere node template'

            self.module.fail_json(msg='Node Template Create request unsuccessful. ' + reason)

        decoded_response = json.loads(resp.read())

        self.results['changed'] = True
        self.results['node_template_id'] = decoded_response['id']

    def template_exists(self):
        headers = {
            'Authorization': 'Bearer ' + self.api_bearer_token,
            'Content-Type': 'application/json'
        }

        query = {
            'name': self.name
        }

        request_type = 'GET'
        url = self.path + '?' + urlencode(query)
        resp, info = fetch_url(self.module, self.rancher_domain + url, headers=headers, method=request_type)

        if info["status"] != 200:
            reason = 'Rancher gave a status code of ' + str(info["status"]) + ' listing existing templates'

            self.module.fail_json(msg='Node Template List request unsuccessful. ' + reason)

        decoded_response = json.loads(resp.read())
        items = len(decoded_response['data'])

        # TODO: Check if there are other numbers of items returned and handle appropriately
        if items == 1:
            return decoded_response['data'][0]['id']

        return False


def main():
    RancherVsphereNodeTemplate()


if __name__ == '__main__':
    main()
